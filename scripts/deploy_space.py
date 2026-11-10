"""
Đưa demo lên Hugging Face Spaces (link công khai cố định, chạy CPU).

    hf auth login                                   # một lần, token quyền write
    python scripts/deploy_space.py --dry-run        # xem sẽ tải lên những gì
    python scripts/deploy_space.py                  # tải checkpoint + tạo/cập nhật Space

Làm hai việc:
  1. Tải checkpoint Reader (mặc định models/r2_ood) lên model repo <user>/<--model-repo>.
  2. Gom app.py, src/, chỉ mục và file trong space/ vào thư mục tạm rồi tải lên Space
     <user>/<--space>; đặt biến QA_MODEL của Space trỏ tới model repo ở bước 1.

Chạy lại lệnh để cập nhật Space sau khi sửa code (thêm --skip-model để khỏi tải lại checkpoint).
"""
from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# File Space cần để chạy app.py (đường dẫn tính từ gốc repo)
SPACE_FILES = [
    "app.py",
    "src/__init__.py",
    "src/pipeline.py",
    "src/retriever/text.py",
    "src/retriever/hybrid.py",
    "src/reader/common.py",
    "src/reader/infer.py",
    "src/eval/metrics.py",
    "src/eval/predictions.py",
    "data/processed/qa_pairs.parquet",      # câu hỏi mẫu
    "data/index_qa/info.json",
    "data/index_qa/meta.parquet",
    "data/index_qa/dense_seg.faiss",
    "data/index_qa/dense_raw.faiss",
]
# File trong space/ đặt ở gốc Space
SPACE_ROOT_FILES = ["README.md", "requirements.txt"]


def stage(dst: Path) -> list[str]:
    """Chép các file của Space vào dst, trả về danh sách đường dẫn tương đối."""
    out = []
    for rel in SPACE_FILES:
        src = ROOT / rel
        if not src.exists():
            if rel == "src/__init__.py":
                continue                            # không bắt buộc
            sys.exit(f"Thiếu {rel}. Chỉ mục tạo bằng: python src/retriever/build_index.py")
        (dst / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst / rel)
        out.append(rel)
    for name in SPACE_ROOT_FILES:
        shutil.copy2(ROOT / "space" / name, dst / name)
        out.append(name)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--checkpoint", default="models/r2_ood")
    ap.add_argument("--model-repo", default="vit5-history-qa", help="tên model repo trên Hub")
    ap.add_argument("--space", default="hoi-dap-lich-su", help="tên Space")
    ap.add_argument("--user", default=None, help="tài khoản/tổ chức HF (mặc định: tài khoản đang đăng nhập)")
    ap.add_argument("--skip-model", action="store_true", help="không tải lại checkpoint")
    ap.add_argument("--dry-run", action="store_true", help="chỉ liệt kê, không tải lên")
    args = ap.parse_args()

    ckpt = ROOT / args.checkpoint
    if not (ckpt / "model.safetensors").exists():
        sys.exit(f"Không thấy checkpoint ở {ckpt}")

    with tempfile.TemporaryDirectory() as tmp:
        files = stage(Path(tmp))
        size = sum((Path(tmp) / f).stat().st_size for f in files) / 1e6
        print(f"Space: {len(files)} file, {size:.1f} MB")
        for f in files:
            print("   ", f)
        ck = [p for p in ckpt.iterdir() if p.name != "training_args.bin"]
        print(f"Checkpoint {args.checkpoint}: {len(ck)} file, "
              f"{sum(p.stat().st_size for p in ck) / 1e6:.0f} MB")
        if args.dry_run:
            print("--dry-run: không tải lên.")
            return

        from huggingface_hub import HfApi
        api = HfApi()
        user = args.user or api.whoami()["name"]    # lỗi ở đây = chưa `hf auth login`
        model_id, space_id = f"{user}/{args.model_repo}", f"{user}/{args.space}"

        if not args.skip_model:
            print(f"Tải checkpoint lên {model_id} ...")
            api.create_repo(model_id, repo_type="model", exist_ok=True)
            api.upload_folder(folder_path=str(ckpt), repo_id=model_id, repo_type="model",
                              ignore_patterns=["training_args.bin"],
                              commit_message="Reader ViT5 (R2 + ViQuAD ngoài miền)")

        print(f"Tạo/cập nhật Space {space_id} ...")
        api.create_repo(space_id, repo_type="space", space_sdk="gradio", exist_ok=True)
        api.add_space_variable(space_id, "QA_MODEL", model_id)
        api.upload_folder(folder_path=tmp, repo_id=space_id, repo_type="space",
                          commit_message="Cập nhật demo")

    print(f"\nXong. Demo: https://huggingface.co/spaces/{space_id}")
    print("Lần đầu Space mất vài phút để cài thư viện và tải model (xem tab Logs).")


if __name__ == "__main__":
    main()
