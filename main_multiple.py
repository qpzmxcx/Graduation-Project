import cv2
import multiprocessing
import os

# 使用两个usb摄像头捕获视频
# 两个摄像头的设备编号分别为 0 和 1
# 每个摄像头捕获 100 帧视频，每 25 帧保存一次
# 每个摄像头的视频保存为 output_camera_0.avi 和 output_camera_1.avi
# 每个视频分别存放在不同的文件中
# 每个视频的分段视频保存在不同的文件中

# 摄像头设备编号
camera_indices = [0, 1] # 摄像头设备编号
frame_count_per_camera = 200  # 每个摄像头要捕获的帧数
frames_per_save = 25  # 每个摄像头每次保存的帧数


# 创建一个队列来存储帧
# 截取并保存指定数量的视频帧
def save_video_segment(camera_idx, queue, output_file, total_frames, frames_per_segment, frames_per_save):
    cap = cv2.VideoCapture(camera_idx)

    # 设置分辨率为 4K (3840x2160)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # 定义视频写入器
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(output_file, fourcc, 30.0, (640, 480))

    frames_saved = 0
    segment_size = total_frames // 4  # 每段视频的帧数
    frames_to_capture = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 将帧加入列表
        frames_to_capture.append(frame)

        # 如果已捕获到当前段的帧数，则保存部分视频
        if len(frames_to_capture) >= segment_size:
            # 从当前分段中截取特定的帧
            selected_frames = frames_to_capture[:frames_per_save]
            for f in selected_frames:
                out.write(f)
            frames_saved += len(selected_frames)
            frames_to_capture = frames_to_capture[frames_per_save:]  # 清空已处理的帧

        if frames_saved >= frames_per_segment:
            break

    cap.release()
    out.release()


# 处理多个摄像头视频的主进程
def main(frame_count_per_camera=100, frames_per_save=25):
    # 创建一个队列来存储帧
    queue = multiprocessing.Queue()

    # 定义每个摄像头的输出文件
    output_files = [f"output_camera_{idx}.avi" for idx in camera_indices]

    # 每个摄像头保存的帧数四等分，每个分段中截取指定的帧数
    for idx, output_file in zip(camera_indices, output_files):
        total_frames = frame_count_per_camera  # 每个摄像头要捕获的帧数
        frames_per_segment = total_frames // 4  # 每段视频的帧数

        # 创建进程来捕获视频帧并保存视频
        p = multiprocessing.Process(target=save_video_segment,
                                    args=(idx, queue, output_file, total_frames, frames_per_segment, frames_per_save))
        p.start()
        p.join()  # 等待该进程完成

    print("视频保存完成。")


if __name__ == "__main__":
    main()
