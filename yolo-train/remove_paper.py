import os
import glob

# 資料集根目錄
ROOT = "./tissue"

# 要保留的類別 ID
KEEP_CLASSES = {1}  # 只保留 TISSUE (class id 1)

def filter_labels(split):
    label_dir = os.path.join(ROOT, split, "labels")
    image_dir = os.path.join(ROOT, split, "images")

    label_files = glob.glob(os.path.join(label_dir, "*.txt"))
    removed_labels = 0
    removed_images = 0
    total_files = len(label_files)

    for label_path in label_files:
        with open(label_path, "r") as f:
            lines = f.readlines()

        # 根據第一個欄位 (class id) 過濾
        filtered_lines = []
        for l in lines:
            parts = l.strip().split()
            if not parts:
                continue
            try:
                class_id = int(float(parts[0]))  # 有些可能是浮點數
            except ValueError:
                continue

            if class_id in KEEP_CLASSES:
                filtered_lines.append(l)

        if not filtered_lines:
            # 沒有任何保留標註 → 刪掉 label + 對應圖片
            os.remove(label_path)
            removed_labels += 1

            # 找對應圖片
            img_name = os.path.splitext(os.path.basename(label_path))[0]
            for ext in [".jpg", ".png", ".jpeg"]:
                img_path = os.path.join(image_dir, img_name + ext)
                if os.path.exists(img_path):
                    os.remove(img_path)
                    removed_images += 1
                    break
        else:
            # 覆寫成只保留 tissue 的內容
            with open(label_path, "w") as f:
                f.writelines(filtered_lines)

    print(f"[{split}] 完成。共 {total_files} 筆標註檔，移除 {removed_labels} 筆無效標註檔與 {removed_images} 張圖片。")

if __name__ == "__main__":
    for split in ["train", "valid", "test"]:
        filter_labels(split)


