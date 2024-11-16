import cv2
import numpy as np
import onnxruntime

class Detect:
    def __init__(self):
        self.onnx_session = onnxruntime.InferenceSession("yolo.onnx")
        self.model_inputs = self.onnx_session.get_inputs()

    def detect(self, img_content):
        confidence_thres = 0.8
        iou_thres = 0.8
        bg_img = cv2.imdecode(np.frombuffer(img_content, np.uint8), cv2.IMREAD_ANYCOLOR)
        img_height, img_width = bg_img.shape[:2]
        bg_img = cv2.resize(bg_img, (320, 320))
        image_data = np.array(bg_img) / 255.0
        image_data = np.transpose(image_data, (2, 0, 1))
        image_data = np.expand_dims(image_data, axis=0).astype(np.float32)
        output = self.onnx_session.run(None, {self.model_inputs[0].name: image_data})
        outputs = np.transpose(np.squeeze(output[0]))
        rows = outputs.shape[0]
        boxes, scores = [], []
        x_factor = img_width / 320
        y_factor = img_height / 320
        for i in range(rows):
            classes_scores = outputs[i][4:]
            max_score = np.amax(classes_scores)
            if max_score >= confidence_thres:
                x, y, w, h = outputs[i][0], outputs[i][1], outputs[i][2], outputs[i][3]
                left = int((x - w / 2) * x_factor)
                top = int((y - h / 2) * y_factor)
                width = int(w * x_factor)
                height = int(h * y_factor)
                boxes.append([left, top, width, height])
                scores.append(max_score)
        indices = cv2.dnn.NMSBoxes(boxes, scores, confidence_thres, iou_thres)
        new_boxes = [boxes[i] for i in indices]
        if len(new_boxes) != 1:
            new_scores = [scores[i] for i in indices]
            max_score_index = np.argmax(new_scores)
            new_boxes = [new_boxes[max_score_index]]
        return new_boxes[0]