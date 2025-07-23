from ultralytics import YOLO
import os
import cv2
import numpy as np
from collections import Counter

# 1. model path
model = YOLO("E:/Anaconda/envs/yolov10uno/models/v10n-runs/weights/best.pt")

# 2. img path
img_path = "E:\Anaconda\envs\yolov10uno\deploy\graph4.png"
image = cv2.imread(img_path)

results = model(img_path, save=False, imgsz=640, conf=0.45)

# color detect due to the datasets lack of classification of clolors
def get_card_color(region):
    hsv = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    # 排除灰度区域（用于排除白色/黑色背景干扰）
    mask = (s > 40) & (v > 50)
    h = h[mask]

    if len(h) == 0:
        return "unknown"

    avg_hue = Counter(h.flatten()).most_common(1)[0][0]
    if 0 <= avg_hue <= 10 or avg_hue >= 160:
        return "red"
    elif 20 <= avg_hue <= 40:
        return "yellow"
    elif 40 < avg_hue <= 85:
        return "green"
    elif 90 <= avg_hue <= 130:
        return "blue"
    
# get results
boxes = results[0].boxes.xyxy.cpu().numpy()
classes = results[0].boxes.cls.cpu().numpy().astype(int)
confidences = results[0].boxes.conf.cpu().numpy()

names = model.names

annotated = image.copy()

colored_labels = []
for box, cls_id, conf in zip(boxes, classes, confidences):
    name = names[cls_id]

    x1, y1, x2, y2 = map(int, box)
    card_crop = image[y1:y2, x1:x2]
    
    # only get non-wild and non-+4 card color
    if "wild" not in name and "+4" not in name:
        card_color = get_card_color(card_crop)
        name = f"{card_color}_{name}"
        
    colored_labels.append(name)
    

    # show results
    cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(annotated, f"{name} {conf:.2f}", (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)

# show img
cv2.imshow("Colored Result", annotated)
cv2.waitKey(0)
cv2.destroyAllWindows()

save_dir = r"E:\Anaconda\envs\yolov10uno\deploy"
save_path = os.path.join(save_dir, "result_with_boxes.jpg")
cv2.imwrite(save_path, annotated)
print(f"img save to: {save_path}")

# print results
counts = Counter(colored_labels)
print("\nDetected cards:")
for label, count in counts.items():
    print(f"{count} {label}")
