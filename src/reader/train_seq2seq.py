"""
Giai đoạn 4: fine-tune Reader ViT5 text-to-text (Seq2SeqTrainer). Cần GPU (Colab).

  R1 — train trên đoạn văn đúng:
    python src/reader/train_seq2seq.py --data r1
  R2 — đoạn đúng + đoạn nhiễu retriever tìm được (đọc data/processed/retrieved_hybrid.parquet):
    python src/reader/train_seq2seq.py --data r2
  Chạy thử trên CPU:
    python src/reader/train_seq2seq.py --data r2 --max_train 32 --max_eval 16 --epochs 1 --no_fp16

Input  = format_input(câu hỏi, đoạn) (src/reader/infer.py — dùng chung với suy luận).
Target = đáp án; câu không trả lời được / đoạn nhiễu không chứa đáp án -> "không có câu trả lời".
Mỗi epoch: sinh greedy trên dev (đoạn đúng), chấm F1 bằng src/eval/metrics.py; giữ checkpoint
F1 cao nhất, early stopping. Model tốt nhất lưu ở output_dir (+ train_config.json: cấu hình,
commit, số mẫu, lịch sử dev). Suy luận sau đó bằng src/reader/infer.py --model <output_dir>.
"""
from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

import pandas as pd
import yaml

from common import ROOT, cache_path, load_corpus_text, load_questions
from infer import format_input
from metrics import NO_ANSWER, aggregate, score
from predictions import git_commit


# ------------------------------------------------------------------ dữ liệu
def target_of(q) -> str:
    return NO_ANSWER if q.is_impossible else q.answer_text


def build_examples(qa: pd.DataFrame, text: dict[str, str], retrieved: pd.DataFrame | None = None,
                   r2: dict | None = None, seed: int = 42) -> pd.DataFrame:
    """
    R1 (retrieved=None): mỗi câu một mẫu (đoạn đúng).
    R2: thêm neg_per_question đoạn nhiễu lấy ngẫu nhiên trong top neg_top_k của retriever
        (bỏ đoạn đúng). Đoạn nhiễu chứa nguyên văn đáp án -> target là đáp án (kind
        "neg_has_answer"), ngược lại target là NO_ANSWER (kind "neg").
    """
    rng = random.Random(seed)
    rows = [{"qa_id": q.qa_id, "context_id": q.context_id, "question": q.question,
             "target": target_of(q), "kind": "gold"} for q in qa.itertuples()]
    if retrieved is not None:
        r2 = r2 or {}
        top_k, n_neg = r2.get("neg_top_k", 5), r2.get("neg_per_question", 1)
        cand = (retrieved[retrieved["rank"] <= top_k].sort_values(["qa_id", "rank"])
                .groupby("qa_id").context_id.apply(list).to_dict())
        for q in qa.itertuples():
            if q.is_impossible and not r2.get("neg_for_impossible", False):
                continue
            negs = [c for c in cand.get(q.qa_id, []) if c != q.context_id]
            for c in rng.sample(negs, min(n_neg, len(negs))):
                has = (not q.is_impossible) and q.answer_text in text[c]
                rows.append({"qa_id": q.qa_id, "context_id": c, "question": q.question,
                             "target": q.answer_text if has else NO_ANSWER,
                             "kind": "neg_has_answer" if has else "neg"})
    df = pd.DataFrame(rows)
    df["source"] = [format_input(q, text[c]) for q, c in zip(df.question, df.context_id)]
    return df


def tokenize(df: pd.DataFrame, tok, cfg):
    enc = tok(list(df.source), max_length=cfg["max_source_length"], truncation=True)
    enc["labels"] = tok(text_target=list(df.target), max_length=cfg["max_target_length"],
                        truncation=True)["input_ids"]
    return dict(enc)


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=str(ROOT / "configs/reader_vit5.yaml"))
    ap.add_argument("--data", choices=["r1", "r2"], default="r1")
    ap.add_argument("--output_dir", default=None)
    ap.add_argument("--max_train", type=int, default=None)
    ap.add_argument("--max_eval", type=int, default=None)
    ap.add_argument("--epochs", type=float, default=None)
    ap.add_argument("--lr", type=float, default=None)
    ap.add_argument("--no_fp16", action="store_true", help="tắt fp16 (khi loss NaN trên T4)")
    ap.add_argument("--resume", action="store_true", help="train tiếp từ checkpoint cuối")
    args = ap.parse_args()

    cfg = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))
    for key in ("epochs", "lr"):
        if getattr(args, key) is not None:
            cfg[key] = getattr(args, key)
    out_dir = Path(args.output_dir or ROOT / cfg["output_dir"].replace("r1_", f"{args.data}_"))
    ckpt_dir = ROOT / "checkpoints" / out_dir.name

    import numpy as np
    import torch
    from datasets import Dataset
    from transformers import (AutoModelForSeq2SeqLM, AutoTokenizer, DataCollatorForSeq2Seq,
                              EarlyStoppingCallback, Seq2SeqTrainer, Seq2SeqTrainingArguments,
                              TrainerCallback, set_seed)
    set_seed(cfg["seed"])
    text = load_corpus_text()

    # --- dữ liệu train / dev
    tr = load_questions("train", args.max_train, seed=cfg["seed"])
    retrieved = None
    if args.data == "r2":
        p = cache_path(cfg["r2"]["mode"])
        if not p.exists():
            raise SystemExit(f"Thiếu {p} — chạy src/retriever/cache_retrieval.py trên máy có index")
        retrieved = pd.read_parquet(p)
    train_df = build_examples(tr, text, retrieved, cfg.get("r2"), seed=cfg["seed"])
    dev = load_questions("dev", args.max_eval, seed=cfg["seed"])
    dev_df = build_examples(dev, text)
    kinds = train_df.kind.value_counts().to_dict()
    n_refuse = int((train_df.target == NO_ANSWER).sum())
    print(f"Train {args.data}: {len(tr)} câu -> {len(train_df)} mẫu {kinds}; "
          f"target từ chối {n_refuse} ({100 * n_refuse / len(train_df):.1f}%)")

    tok = AutoTokenizer.from_pretrained(cfg["model"])
    model = AutoModelForSeq2SeqLM.from_pretrained(cfg["model"])
    ds_train = Dataset.from_dict(tokenize(train_df, tok, cfg))
    ds_dev = Dataset.from_dict(tokenize(dev_df, tok, cfg))
    n_cut = sum(len(x) >= cfg["max_source_length"] for x in ds_train["input_ids"])
    print(f"Input bị cắt ở {cfg['max_source_length']} token: {n_cut} mẫu "
          f"({100 * n_cut / len(ds_train):.1f}%)")

    golds = [([] if q.is_impossible else [q.answer_text], bool(q.is_impossible))
             for q in dev.itertuples()]
    dev_labels = [list(x) for x in ds_dev["labels"]]

    def strip_pad(row) -> list[int]:
        return [int(t) for t in row if t >= 0 and t != tok.pad_token_id]

    def compute_metrics(ev):
        # Chốt chặn: dự đoán phải cùng thứ tự với golds (lỗi cũ: group_by_length xáo cả dev).
        labels = [strip_pad(r) for r in ev.label_ids]
        bad = sum(a != strip_pad(b) for a, b in zip(labels, dev_labels))
        if len(labels) != len(dev_labels) or bad:
            raise RuntimeError(f"Thứ tự dev bị xáo: {bad}/{len(labels)} nhãn không khớp")
        preds = ev.predictions[0] if isinstance(ev.predictions, tuple) else ev.predictions
        preds = np.where(preds < 0, tok.pad_token_id, preds)
        texts = [t.strip() for t in tok.batch_decode(preds, skip_special_tokens=True)]
        rows = [{**score(p, g, imp), "is_impossible": imp} for p, (g, imp) in zip(texts, golds)]
        m = aggregate(rows)
        return {"em": m["EM"], "f1": m["F1"], "hasans_f1": m["HasAns_F1"],
                "noans_acc": m["NoAns_acc"], "hasans_abstain": m["HasAns_abstain"]}

    class NaNStop(TrainerCallback):
        nan = False

        def on_log(self, a, state, control, logs=None, **kw):
            if logs and "loss" in logs and not math.isfinite(logs["loss"]):
                NaNStop.nan = True
                control.should_training_stop = True

    cuda = torch.cuda.is_available()
    bf16 = bool(cfg.get("bf16")) and cuda and torch.cuda.is_bf16_supported()
    fp16 = bool(cfg.get("fp16")) and cuda and not bf16 and not args.no_fp16
    print(f"Thiết bị: {'cuda ' + torch.cuda.get_device_name() if cuda else 'cpu'}; "
          f"bf16={bf16} fp16={fp16}")
    targs = Seq2SeqTrainingArguments(
        output_dir=str(ckpt_dir), learning_rate=cfg["lr"], num_train_epochs=cfg["epochs"],
        per_device_train_batch_size=cfg["batch_size"], gradient_accumulation_steps=cfg["grad_accum"],
        per_device_eval_batch_size=cfg["eval_batch_size"], warmup_ratio=cfg["warmup_ratio"],
        weight_decay=cfg["weight_decay"], label_smoothing_factor=cfg["label_smoothing"],
        bf16=bf16, fp16=fp16, seed=cfg["seed"], group_by_length=True,
        eval_strategy="epoch", save_strategy="epoch", save_total_limit=2,
        load_best_model_at_end=True, metric_for_best_model="f1", greater_is_better=True,
        predict_with_generate=True, generation_max_length=cfg["max_target_length"],
        generation_num_beams=cfg["eval_num_beams"], logging_steps=50, report_to=[])
    class Trainer(Seq2SeqTrainer):
        # group_by_length chỉ áp cho train; transformers 4.57 áp cả cho eval (LengthGroupedSampler
        # có ngẫu nhiên) -> dự đoán lệch thứ tự golds, F1 dev vô nghĩa. Dev luôn đi tuần tự.
        def _get_eval_sampler(self, eval_dataset):
            from torch.utils.data import SequentialSampler
            return SequentialSampler(eval_dataset)

    trainer = Trainer(
        model=model, args=targs, train_dataset=ds_train, eval_dataset=ds_dev,
        data_collator=DataCollatorForSeq2Seq(tok, model=model), processing_class=tok,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(cfg["early_stopping_patience"]), NaNStop()])
    trainer.train(resume_from_checkpoint=args.resume or None)
    if NaNStop.nan:
        raise SystemExit("Loss NaN (thường do fp16 với T5) -> chạy lại với --no_fp16")

    trainer.save_model(str(out_dir))
    tok.save_pretrained(out_dir)
    hist = [h for h in trainer.state.log_history if "eval_f1" in h]
    info = {"data": args.data, "commit": git_commit(), "config": cfg,
            "n_train_questions": len(tr), "n_train_examples": len(train_df), "kinds": kinds,
            "n_target_refuse": n_refuse, "n_dev": len(dev), "device": "cuda" if cuda else "cpu",
            "bf16": bf16, "fp16": fp16, "best_checkpoint": trainer.state.best_model_checkpoint,
            "best_dev_f1": trainer.state.best_metric, "dev_history": hist}
    (out_dir / "train_config.json").write_text(json.dumps(info, indent=2, ensure_ascii=False),
                                               encoding="utf-8")
    print("Dev theo epoch (đoạn đúng, greedy):")
    for h in hist:
        print(f"  epoch {h['epoch']:.1f}: EM {h['eval_em']:.1f}  F1 {h['eval_f1']:.1f}  "
              f"HasAns-F1 {h['eval_hasans_f1']:.1f}  NoAns {h['eval_noans_acc']:.1f}")
    print(f"Model tốt nhất (F1 {trainer.state.best_metric}) -> {out_dir}")


if __name__ == "__main__":
    main()
