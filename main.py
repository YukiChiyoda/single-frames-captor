import os
import cv2
import numpy as np


def detect_faces(image):
    # 加载人脸检测器
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    # 转换为灰度图像进行检测
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 检测人脸
    faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(100, 100))

    if len(faces) > 0:
        # 返回所有检测到的人脸的中心点的平均值和人脸位置列表
        centers = [(y + h // 2) for (x, y, w, h) in faces]
        return int(np.mean(centers)), faces
    return None, []


def crop_to_4_3_ratio(image, face_center=None):
    height, width = image.shape[:2]
    target_ratio = 4 / 3

    # 计算以当前宽度为基准的目标高度
    target_height = int(width / target_ratio)

    # 如果目标高度小于等于原始高度，需要考虑人脸位置
    if target_height <= height:
        if face_center is not None:
            # 计算裁剪窗口的中心应该在的位置
            crop_center = target_height // 2
            # 计算需要的偏移量，使人脸位于中心
            offset = face_center - crop_center

            # 确保裁剪窗口不会超出图像边界
            start_y = max(0, offset)
            end_y = start_y + target_height
            if end_y > height:
                start_y = height - target_height
                end_y = height

            cropped_image = image[start_y:end_y, 0:width]
        else:
            # 如果没有检测到人脸，从五分之一处裁剪
            cropped_image = image[height // 5 : height // 5 + target_height, 0:width]
    else:
        # 如果需要以高度为基准来调整宽度
        target_width = int(height * target_ratio)
        # 计算需要裁剪的两侧宽度
        start_x = (width - target_width) // 2
        cropped_image = image[0:height, start_x : start_x + target_width]

    return cropped_image


def extract_first_frame(input_folder, frame_number=60, crop_frame=True):
    # 遍历文件夹中的所有文件
    for file_name in os.listdir(input_folder):
        # 检查文件是否是 .mp4 文件
        if file_name.endswith(".mp4"):
            video_path = os.path.join(input_folder, file_name)
            # 打开视频文件
            video_capture = cv2.VideoCapture(video_path)
            if not video_capture.isOpened():
                print(f"无法打开视频文件: {file_name}")
                continue

            # 读取指定帧
            video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1)
            success, frame = video_capture.read()
            if success:
                if crop_frame:
                    # 检测人脸位置
                    face_center, faces = detect_faces(frame)

                    # 保存带有人脸标记的原始图像用于调试
                    debug_frame = frame.copy()
                    for x, y, w, h in faces:
                        # 在图像上绘制人脸矩形
                        cv2.rectangle(
                            debug_frame, (x, y), (x + w, y + h), (255, 0, 0), 2
                        )
                        # 绘制中心点
                        center_y = y + h // 2
                        cv2.line(
                            debug_frame,
                            (0, center_y),
                            (frame.shape[1], center_y),
                            (0, 255, 0),
                            1,
                        )

                    debug_output_path = os.path.join(
                        f"{input_folder}debug/debug_{os.path.splitext(file_name)[0]}.jpg",
                    )
                    cv2.imwrite(debug_output_path, debug_frame)
                    print(f"已保存调试图像到: {debug_output_path}")

                    # 裁剪为4:3比例，考虑人脸位置
                    cropped_frame = crop_to_4_3_ratio(frame, face_center)
                else:
                    cropped_frame = frame

                # 构造输出的图片路径
                output_file_name = os.path.splitext(file_name)[0] + ".jpg"
                output_path = os.path.join(input_folder, output_file_name)
                # 保存裁剪后的帧为 jpg 文件
                cv2.imwrite(output_path, cropped_frame)
                print(f"已保存第 {frame_number} 帧到: {output_path}")
            else:
                print(f"无法读取视频文件的第 {frame_number} 帧: {file_name}")
            # 释放视频对象
            video_capture.release()


# 指定目标文件夹路径
input_folder = "./"  # 替换为你的文件夹路径
extract_first_frame(input_folder)
