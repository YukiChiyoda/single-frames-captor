import os
import cv2


def extract_first_frame(input_folder, frame_number=60):
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

            # 读取第一帧
            video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1)
            success, frame = video_capture.read()
            if success:
                # 构造输出的图片路径
                output_file_name = os.path.splitext(file_name)[0] + ".jpg"
                output_path = os.path.join(input_folder, output_file_name)

                # 保存第一帧为 jpg 文件
                cv2.imwrite(output_path, frame)
                print(f"保存第 {frame_number} 帧到: {output_path}")
            else:
                print(f"无法读取视频文件的第 {frame_number} 帧: {file_name}")

            # 释放视频对象
            video_capture.release()


# 指定目标文件夹路径
input_folder = "./"  # 替换为你的文件夹路径
extract_first_frame(input_folder)
