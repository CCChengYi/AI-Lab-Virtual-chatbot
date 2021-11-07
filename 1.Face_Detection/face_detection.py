# coding=utf-8

# 使用保存好的模型

import tensorflow.compat.v1 as tf

tf.disable_v2_behavior()
import numpy as np
import gender_train_data as train_data
import matplotlib.pyplot as plt
import os
import cv2

np.set_printoptions(suppress=True)

##############加载模型#################
sess = tf.compat.v1.Session()
graph_path = os.path.abspath('./model/my-gender-v1.0.meta')
model = os.path.abspath('./model/')

server = tf.train.import_meta_graph(graph_path)
server.restore(sess, tf.train.latest_checkpoint(model))

graph = tf.get_default_graph()



################摄像头检测人脸#######################
cap = cv2.VideoCapture(0)

# 识别出人脸后要画的边框的颜色，RGB格式
color = (0, 255, 0)

num = 0
while cap.isOpened():
        ok, frame = cap.read()  # 读取一帧数据
        if not ok:
                break

        x = graph.get_tensor_by_name('input_images:0')
        y = graph.get_tensor_by_name('input_labels:0')

        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 将当前桢图像转换成灰度图像

        # 人脸检测，1.2和2分别为图片缩放比例和需要检测的有效点数
        faceRects = sess.run(y,feed_dict = {x: frame, y: 1})
        if len(faceRects) > 0:  # 大于0则检测到人脸
                for faceRect in faceRects:  # 单独框出每一张人脸
                        x, y, w, h = faceRect

                        # 将当前帧保存为图片
                        img_name = './pic.jpg'
                        image = frame[y - 10: y + h + 10, x - 10: x + w + 10]
                        cv2.imwrite(img_name, image)

                        num += 1
                        if num > (10):  # 如果超过指定最大保存数量退出循环
                                break

                        # 画出矩形框
                        cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, 2)

                        # 显示当前捕捉到了多少人脸图片了，这样站在那里被拍摄时心里有个数，不用两眼一抹黑傻等着
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        cv2.putText(frame, 'num:%d' % (num), (x + 30, y + 30), font, 1, (255, 0, 255), 4)

                        # 超过指定最大保存数量结束程序
        if num > (10): break

        # 显示图像
        cv2.imshow('face', frame)
        c = cv2.waitKey(10)
        if c & 0xFF == ord('q'):
                break

                # 释放摄像头并销毁所有窗口
cap.release()
cv2.destroyAllWindows()

