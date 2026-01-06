from pathlib import Path

from ultralytics import YOLO
import kagglehub

def main():
    # 訓練資料來源 https://universe.roboflow.com/armat/clean-unclean/dataset/2
    # 記得先執行 change_label_id_to_zero.py, remove_paper.py 把原始資料集中的 paper 資料移除
    # 然後把 tissue/data.yaml 也改成只有一個類別
    path = "data"
    dataset_dir = Path(path)
    data_yaml = dataset_dir / "data.yaml"
    if not data_yaml.exists():
        raise FileNotFoundError(f"❌ 找不到 {data_yaml}")

    # fix_data_yaml(data_yaml)

    # === Step 3. 建立 YOLO 模型並訓練 ===
    model = YOLO("yolo11m.pt")  # 可換 yolov8s.pt 等
    model.train(
        data=str(data_yaml),
        epochs=50,
        imgsz=640,
        batch=32,
        device=0,   # GPU=0, 或 -1 表示用 CPU
        project="runs/train",
        name="tissue",
        translate=0.1, scale=0.1, fliplr=0.5, flipud=0.5,
    )
    
    # === 手動保存模型 ===
    # 方法1: 保存到指定路徑
    model.save("tissue_model.pt")
    print("✅ 模型已保存到 tissue_model.pt")
    
    # 方法2: 使用訓練好的模型路徑 (通常在 runs/train/tissue/weights/)
    trained_model = YOLO("runs/train/tissue/weights/best.pt")
    print("✅ 載入訓練好的最佳模型")
    

    # # === Step 4. 驗證與推論 ===
    # metrics = model.val()
    # print("✅ 驗證完成:", metrics)


if __name__ == "__main__":
    main()


