import argparse
import functools
import os
import time

import cv2
import numpy as np
import torch
from PIL import ImageDraw, ImageFont, Image

from detection.face_detect import MTCNN
from utils.utils import add_arguments, print_arguments

parser = argparse.ArgumentParser(description=__doc__)
add_arg = functools.partial(add_arguments, argparser=parser)
add_arg('camera_id', int, 1, '使用的相机ID')
add_arg('face_db_path', str, 'face_db', '人脸库路径')
add_arg('threshold', float, 0.6, '判断相识度的阈值')
add_arg('mobilefacenet_model_path', str, 'save_model/mobilefacenet.pth', 'MobileFaceNet预测模型的路径')
add_arg('mtcnn_model_path', str, 'save_model/mtcnn', 'MTCNN预测模型的路径')
args = parser.parse_args()
print_arguments(args)


class Predictor:
    def __init__(self, mtcnn_model_path, mobilefacenet_model_path, face_db_path, threshold=0.7):
        self.threshold = threshold
        self.mtcnn = MTCNN(model_path=mtcnn_model_path)
        self.device = torch.device("cpu")

        # 加载模型
        self.model = torch.jit.load(mobilefacenet_model_path, map_location='cpu')
        self.model.to(self.device)
        self.model.eval()

        self.faces_db = self.load_face_db(face_db_path)

    def load_face_db(self, face_db_path):
        faces_db = {}
        for path in os.listdir(face_db_path):
            name = os.path.basename(path).split('.')[0]
            image_path = os.path.join(face_db_path, path)
            img = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), -1)
            imgs, _ = self.mtcnn.infer_image(img)
            if imgs is None or len(imgs) > 1:
                print('人脸库中的 %s 图片包含不是1张人脸，自动跳过该图片' % image_path)
                continue
            imgs = self.process(imgs)
            feature = self.infer(imgs[0])
            faces_db[name] = feature[0][0]
        return faces_db

    @staticmethod
    def process(imgs):
        imgs1 = []
        for img in imgs:
            img = img.transpose((2, 0, 1))
            img = (img - 127.5) / 127.5
            imgs1.append(img)
        return imgs1

    # 预测图片
    def infer(self, imgs):
        assert len(imgs.shape) == 3 or len(imgs.shape) == 4
        if len(imgs.shape) == 3:
            imgs = imgs[np.newaxis, :]
        features = []
        for i in range(imgs.shape[0]):
            img = imgs[i][np.newaxis, :]
            img = torch.tensor(img, dtype=torch.float32, device=self.device)
            # 执行预测
            feature = self.model(img)
            feature = feature.detach().cpu().numpy()
            # print(feature.shape)
            features.append(feature)
        return features

    def recognition(self, img):
        imgs, boxes = self.mtcnn.infer_image(img)
        if imgs is None:
            return None, None
        imgs = self.process(imgs)
        imgs = np.array(imgs, dtype='float32')
        features = self.infer(imgs)
        names = []
        probs = []
        NPresults = []
        for i in range(len(features)):
            feature = features[i][0]
            results_dict = {}
            for name in self.faces_db.keys():
                feature1 = self.faces_db[name]
                prob = np.dot(feature, feature1) / (np.linalg.norm(feature) * np.linalg.norm(feature1))
                results_dict[name] = prob
            results = sorted(results_dict.items(), key=lambda d: d[1], reverse=True)
            print('人脸对比结果：', results)
            result = results[0]
            prob = float(result[1])
            probs.append(prob)
            if prob > self.threshold:
                name = result[0]
                names.append(name)
                NPresults.append((name, prob))
            else:
                names.append('unknow')
                name = u'unknow'
                NPresults.append((name, prob))
        # NPresult = sorted(NPresult_dict.items(), key=lambda d: d[1], reverse=True)
        return boxes, NPresults

    def add_text(self, img, text, left, top, color=(0, 0, 0), size=20):
        if isinstance(img, np.ndarray):
            img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('simfang.ttf', size)  # 字体
        draw.text((left, top), text, color, font=font)
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # 画出人脸框和关键点
    def draw_face(self, img, boxes_c, names):
        if boxes_c is not None:
            print(boxes_c)
            for i in range(boxes_c.shape[0]):
                bbox = boxes_c[i, :4]
                name = names[i]
                print(bbox)
                print(name)
                corpbbox = [int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])]
                print(corpbbox)
                # 画人脸框
                cv2.rectangle(img, (corpbbox[0], corpbbox[1]),
                              (corpbbox[2], corpbbox[3]), (0, 255, 0), 1)
                # 判别为人脸的名字
                img = self.add_text(img, name, corpbbox[0], corpbbox[1] - 15, color=(0, 255, 0), size=18)
                print(name)
        return img


# ShowPredictor = Predictor(args.mtcnn_model_path, args.mobilefacenet_model_path, args.face_db_path,
#                           threshold=args.threshold)

if __name__ == '__main__':
    predictor = Predictor(args.mtcnn_model_path, args.mobilefacenet_model_path, args.face_db_path,
                          threshold=args.threshold)
    cap = cv2.VideoCapture(args.camera_id, cv2.CAP_DSHOW)
    cap.set(6, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))  # 读入mjpg
    cap.set(5, 120)  # 帧率
    cap.set(3, 400)  # 帧宽
    cap.set(4, 400)  # 帧高
    # 自定义模糊
    kernel = np.array([[0, -1, 0], [-1, 2, -1], [0, -1, 0]], np.float32)
    while True:
        ret, img = cap.read()
        if ret:
            start = time.time()
            boxes, NPresult = predictor.recognition(img)
            if boxes is not None:
                img = predictor.draw_face(img, boxes, NPresult[0])
                print('预测的人脸位置：', boxes.astype('int32').tolist())
                print('识别的人脸名称：', NPresult[0])
                print('总识别时间：%dms' % int((time.time() - start) * 1000))
                # cv2.imshow("result", img)
                # cv2.waitKey(1)

            cv2.imshow("result", img)
            cv2.waitKey(1)
