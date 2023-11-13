from ultralytics import YOLO
from PIL import Image

model = YOLO("D:/GitHub/Rozpoznawanie_obrazow/RozpoznawanieRasPsow/Models/YoloV8_own//best.pt")

results = model.predict("D:/GitHub/Rozpoznawanie_obrazow/RozpoznawanieRasPsow/Pictures/germanShepherd.jpg")
result = results[0]
len(result.boxes)
box = result.boxes[0]

# print("Object type:",box.cls[0])
# print("Coordinates:",box.xyxy[0])
# print("Probability:",box.conf[0])
# print(result.names)

for box in result.boxes:
    class_id = result.names[box.cls[0].item()]
    cords = box.xyxy[0].tolist()
    cords = [round(x) for x in cords]
    conf = round(box.conf[0].item(), 2)
    print("Object type:", class_id)
    print("Coordinates:", cords)
    print("Probability:", conf)
    print("---")

Image.fromarray(result.plot()[:, :, ::-1]).show()

