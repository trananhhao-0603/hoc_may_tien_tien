"""
Baseline B1: fine-tune Reader trích xuất (xlm-roberta-base) kiểu squad_v2 trên đoạn văn đúng,
theo HF question-answering tutorial. Cần GPU (Colab T4 ~ 25 phút / 3 epoch).

    # train trên train, dự đoán dev (đoạn đúng) -> data/predictions/b1_gold_dev.jsonl
    python src/reader/train_extractive.py --config configs/reader_extractive.yaml --tune_threshold
    # chỉ dự đoán với checkpoint có sẵn, trên đoạn retriever tìm được
    python src/reader/train_extractive.py --predict_only models/b1_xlmr --context retrieved --k 3
    # chạy thử trên CPU
    python src/reader/train_extractive.py --max_train 64 --max_eval 32 --epochs 1

Câu không trả lời được: nhãn span = token <s> (vị trí 0). Lúc dự đoán so điểm null
(start[0] + end[0]) với span tốt nhất; ngưỡng có thể chọn trên dev (--tune_threshold).
"""
from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path

import numpy as np
import yaml

from common import ROOT, get_contexts, load_corpus_text, load_questions
from metrics import NO_ANSWER, aggregate, score
from predictions import PRED_DIR, gold_fields, write_predictions


# ------------------------------------------------------------------ dữ liệu
def train_features(qa, text, tok, cfg):
    """Tokenize (câu hỏi, đoạn) có cắt trượt; gán vị trí start/end token cho mỗi feature."""
    enc = tok(list(qa.question), [text[c] for c in qa.context_id], truncation="only_second",
              max_length=cfg["max_length"], stride=cfg["doc_stride"],
              return_overflowing_tokens=True, return_offsets_mapping=True, padding="max_length")
    smap = enc.pop("overflow_to_sample_mapping")
    starts, ends = [], []
    for i, offsets in enumerate(enc["offset_mapping"]):
        q = qa.iloc[smap[i]]
        seq = enc.sequence_ids(i)
        if q.is_impossible or not q.answer_span_ok:
            starts.append(0); ends.append(0); continue
        a0 = int(q.answer_start); a1 = a0 + len(q.answer_text)
        c0 = seq.index(1); c1 = len(seq) - 1 - seq[::-1].index(1)
        if not (offsets[c0][0] <= a0 and offsets[c1][1] >= a1):     # đáp án không nằm trong feature
            starts.append(0); ends.append(0); continue
        s = c0
        while s <= c1 and offsets[s][0] <= a0:
            s += 1
        e = c1
        while e >= c0 and offsets[e][1] >= a1:
            e -= 1
        starts.append(s - 1); ends.append(e + 1)
    enc.pop("offset_mapping")
    enc["start_positions"], enc["end_positions"] = starts, ends
    return enc


def eval_features(questions, passages, tok, cfg):
    enc = tok(questions, passages, truncation="only_second", max_length=cfg["max_length"],
              stride=cfg["doc_stride"], return_overflowing_tokens=True,
              return_offsets_mapping=True, padding="max_length")
    smap = enc.pop("overflow_to_sample_mapping")
    # chỉ giữ offset của phần đoạn văn (để không chọn span trong câu hỏi)
    enc["offset_mapping"] = [[o if s == 1 else None for o, s in zip(off, enc.sequence_ids(i))]
                             for i, off in enumerate(enc["offset_mapping"])]
    return enc, list(smap)


def postprocess(n_pairs, passages, enc, smap, start_logits, end_logits, cfg):
    """-> list (đáp án tốt nhất, điểm span, điểm null) cho từng cặp (câu, đoạn)."""
    feats = collections.defaultdict(list)
    for f, s in enumerate(smap):
        feats[s].append(f)
    out, nb, maxlen = [], cfg["n_best"], cfg["max_answer_length"]
    for i in range(n_pairs):
        best, best_score, null = "", -1e9, 1e9
        for f in feats[i]:
            sl, el, off = start_logits[f], end_logits[f], enc["offset_mapping"][f]
            null = min(null, float(sl[0] + el[0]))
            for s in np.argsort(sl)[-nb:][::-1]:
                for e in np.argsort(el)[-nb:][::-1]:
                    if off[s] is None or off[e] is None or e < s or e - s + 1 > maxlen:
                        continue
                    sc = float(sl[s] + el[e])
                    if sc > best_score:
                        best_score, best = sc, passages[i][off[s][0]:off[e][1]]
        out.append((best, best_score, null))
    return out


# ------------------------------------------------------------------ dự đoán
def predict(model, tok, qa, ctxs, text, cfg, batch_size=64):
    import torch
    pairs = [(i, c["context_id"]) for i, cs in enumerate(ctxs) for c in cs]
    qs = [qa.question[i] for i, _ in pairs]
    ps = [text[c] for _, c in pairs]
    enc, smap = eval_features(qs, ps, tok, cfg)
    device = next(model.parameters()).device
    model.eval()
    S, E = [], []
    with torch.inference_mode():
        for b in range(0, len(smap), batch_size):
            inp = {k: torch.tensor(enc[k][b:b + batch_size]).to(device)
                   for k in ("input_ids", "attention_mask")}
            o = model(**inp)
            S.append(o.start_logits.float().cpu().numpy()); E.append(o.end_logits.float().cpu().numpy())
    res = postprocess(len(pairs), ps, enc, smap, np.concatenate(S), np.concatenate(E), cfg)
    per_q = collections.defaultdict(list)
    for (i, cid), (ans, sc, null) in zip(pairs, res):
        per_q[i].append({"context_id": cid, "answer": ans, "score": sc, "null": null})
    return per_q


def decide(cands, threshold):
    """Chọn đoạn có span điểm cao nhất; từ chối nếu null - span > threshold ở đoạn đó."""
    best = max(cands, key=lambda c: c["score"])
    if not best["answer"] or best["null"] - best["score"] > threshold:
        return NO_ANSWER, None
    return best["answer"], best["context_id"]


def tune_threshold(qa, per_q):
    """Ngưỡng tối ưu F1 trên tập đang dự đoán (chỉ dùng với dev)."""
    diffs = sorted({round(c["null"] - c["score"], 3) for cs in per_q.values() for c in cs})
    grid = np.unique(np.quantile(diffs, np.linspace(0, 1, 101))) if diffs else [0.0]
    best_t, best_f1 = 0.0, -1
    for t in list(grid) + [0.0]:
        rows = []
        for i, q in enumerate(qa.itertuples()):
            pred, _ = decide(per_q[i], t)
            gold = [] if q.is_impossible else [q.answer_text]
            rows.append({**score(pred, gold, q.is_impossible), "is_impossible": q.is_impossible})
        f1 = aggregate(rows)["F1"]
        if f1 > best_f1:
            best_t, best_f1 = float(t), f1
    print(f"Ngưỡng null tốt nhất: {best_t:.3f} (F1 {best_f1:.2f})")
    return best_t


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=str(ROOT / "configs/reader_extractive.yaml"))
    ap.add_argument("--predict_only", default=None, help="đường dẫn checkpoint, bỏ qua train")
    ap.add_argument("--split", default="dev", help="split để dự đoán")
    ap.add_argument("--context", choices=["gold", "retrieved"], default="gold")
    ap.add_argument("--mode", default="hybrid")
    ap.add_argument("--k", type=int, default=1)
    ap.add_argument("--tune_threshold", action="store_true", help="chọn ngưỡng null trên dev")
    ap.add_argument("--threshold", type=float, default=None)
    ap.add_argument("--max_train", type=int, default=None)
    ap.add_argument("--max_eval", type=int, default=None)
    ap.add_argument("--epochs", type=float, default=None)
    ap.add_argument("--run", default=None)
    args = ap.parse_args()

    cfg = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))
    if args.epochs is not None:
        cfg["epochs"] = args.epochs
    import torch
    from transformers import (AutoModelForQuestionAnswering, AutoTokenizer, Trainer,
                              TrainingArguments, default_data_collator, set_seed)
    set_seed(cfg["seed"])
    text = load_corpus_text()
    out_dir = Path(args.predict_only or ROOT / cfg["output_dir"])

    if args.predict_only:
        tok = AutoTokenizer.from_pretrained(out_dir)
        model = AutoModelForQuestionAnswering.from_pretrained(out_dir)
        thr_file = out_dir / "null_threshold.json"
        if args.threshold is None and thr_file.exists():
            cfg["null_threshold"] = json.loads(thr_file.read_text())["threshold"]
    else:
        from datasets import Dataset
        tok = AutoTokenizer.from_pretrained(cfg["model"])
        model = AutoModelForQuestionAnswering.from_pretrained(cfg["model"])
        tr = load_questions("train", args.max_train, seed=cfg["seed"])
        tr = tr[tr.is_impossible | tr.answer_span_ok].reset_index(drop=True)
        ds = Dataset.from_dict(dict(train_features(tr, text, tok, cfg)))
        print(f"Train: {len(tr)} câu -> {len(ds)} feature")
        bf16 = bool(cfg.get("bf16")) and torch.cuda.is_available() and torch.cuda.is_bf16_supported()
        targs = TrainingArguments(
            output_dir=str(out_dir), learning_rate=cfg["lr"], num_train_epochs=cfg["epochs"],
            per_device_train_batch_size=cfg["batch_size"],
            gradient_accumulation_steps=cfg["grad_accum"], warmup_ratio=cfg["warmup_ratio"],
            weight_decay=cfg["weight_decay"], bf16=bf16,
            fp16=torch.cuda.is_available() and not bf16, seed=cfg["seed"],
            save_strategy="no", logging_steps=50, report_to=[])
        Trainer(model=model, args=targs, train_dataset=ds,
                data_collator=default_data_collator).train()
        model.save_pretrained(out_dir); tok.save_pretrained(out_dir)
        (out_dir / "train_config.json").write_text(json.dumps(cfg, indent=2), encoding="utf-8")

    if not torch.cuda.is_available():
        model.to("cpu")
    else:
        model.to("cuda")
    qa = load_questions(args.split, args.max_eval)
    k = 1 if args.context == "gold" else args.k
    ctxs, ret_ms = get_contexts(qa, args.context, k=k, mode=args.mode)
    per_q = predict(model, tok, qa, ctxs, text, cfg)

    thr = cfg["null_threshold"] if args.threshold is None else args.threshold
    if args.tune_threshold:
        if args.split != "dev":
            raise SystemExit("--tune_threshold chỉ dùng trên dev")
        thr = tune_threshold(qa, per_q)
        (out_dir / "null_threshold.json").write_text(json.dumps({"threshold": thr}))

    rows = []
    for i, q in enumerate(qa.itertuples()):
        pred, used = decide(per_q[i], thr)
        rows.append({**gold_fields(q), "prediction": pred, "context_source": args.context,
                     "contexts": ctxs[i], "used_context_id": used,
                     "latency_ms": {"retrieve": ret_ms}, "extra": {"per_context": per_q[i]}})
    run = args.run or f"b1_{args.context}" + (f"_k{k}" if args.context == "retrieved" else "") + f"_{args.split}"
    write_predictions(PRED_DIR / f"{run}.jsonl", rows,
                      meta={**vars(args), "run": run, "model": cfg["model"], "checkpoint": str(out_dir),
                            "null_threshold": thr, "config": cfg})


if __name__ == "__main__":
    main()
