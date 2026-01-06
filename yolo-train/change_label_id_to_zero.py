import os
import glob

# === 設定資料集根目錄 ===
ROOT = "./tissue"

def change_label_ids(split):
    label_dir = os.path.join(ROOT, split, "labels")
    label_files = glob.glob(os.path.join(label_dir, "*.txt"))
    total_files = len(label_files)
    modified = 0

    for label_path in label_files:
        with open(label_path, "r") as f:
            lines = f.readlines()

        new_lines = []
        for l in lines:
            parts = l.strip().split()
            if not parts:
                continue
            # 把第一個欄位（class id）改成 0
            parts[0] = "0"
            new_lines.append(" ".join(parts) + "\n")

        # 覆寫回原檔案
        with open(label_path, "w") as f:
            f.writelines(new_lines)
        modified += 1

    print(f"[{split}] 已修改 {modified}/{total_files} 個標註檔。")

if __name__ == "__main__":
    for split in ["train", "valid", "test"]:
        change_label_ids(split)

    # 如果有 cache 檔就刪除
    cache_path = os.path.join(ROOT, "labels.cache")
    if os.path.exists(cache_path):
        os.remove(cache_path)
        print("已刪除舊的 labels.cache。")

    print("✅ 全部修改完成！")


