import cv2
import os

# 打开 USB 摄像头
cap = cv2.VideoCapture(0)
output_folder = './output_frames/'

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# 设置分辨率为 4K (3840x2160)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)

# 定义视频编码方式和输出文件名
fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # MJPEG 编码器，通常支持较高分辨率
out = cv2.VideoWriter('./output_videos/output.avi', fourcc, 30.0, (3840, 2160))  # 输出文件名，帧率30.0，分辨率3840x2160


frames_to_save = 201  # 每个视频保存 100 帧（大约 5 秒）
time_total = frames_to_save / 20

for _ in range(frames_to_save):
    ret, frame = cap.read()  # 读取帧
    if not ret:  # 如果读取失败，退出
        break
    out.write(frame)  # 保存帧

print(f"successfully saved{time_total}Second video")

out.release()
cap.release()
cv2.destroyAllWindows()

# 视频文件路径
video_path = './output_videos/output.avi'

# 需要截取的帧数列表
frame_1 = frames_to_save / 4 * 1 - 1
frame_2 = frames_to_save / 4 * 2 - 1
frame_3 = frames_to_save / 4 * 3 - 1
frame_4 = frames_to_save / 4 * 4 - 1
frame_numbers = [frame_1, frame_2, frame_3, frame_4]  # 例如特定帧率

# 打开视频文件
cap = cv2.VideoCapture(video_path)

# 检查视频是否成功打开
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# 获取视频的总帧数
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f"Total frames in the video: {total_frames}")

frame_num0 = 0

# 遍历所有需要的帧数
for frame_num in frame_numbers:
    # 确保帧数在有效范围内
    if frame_num >= total_frames:
        print(f"Frame {frame_num} is out of range.")
        continue

    # 定位到指定帧
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)

    # 读取指定帧
    ret, frame = cap.read()

    # 如果读取成功，保存帧为图片
    if ret:
        # 保存图片，文件名为：frame_帧数.jpg
        frame_filename = os.path.join(output_folder, f"frame_{frame_num0}.jpg")
        cv2.imwrite(frame_filename, frame)
        print(f"Frame {frame_num0} saved as {frame_filename}")
        frame_num0 += 1
    else:
        print(f"Failed to read frame {frame_num0}")

# 释放资源并关闭窗口
cap.release()
