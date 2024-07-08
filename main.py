import cv2
import moviepy.editor as mp
import numpy as np
from PIL import Image
import shutil
import os

def pixelate(image, pixel_size):
    image = Image.fromarray(image)

    small = image.resize(
        (image.width // pixel_size, image.height // pixel_size),
        Image.NEAREST
    )
    result = small.resize(
        (image.width, image.height),
        Image.NEAREST
    )
    return np.array(result)

def convert_to_pixel_art(input_video_path, output_video_path, pixel_size=16):

    tmp_output_video_path = "./tmp/tmp_output_video.mp4"
    tmp_output_audio_path = "./tmp/tmp_output_audio.mp3"

    cap = cv2.VideoCapture(input_video_path)

    if not cap.isOpened():
        print("Error opening video file")
        return

    # tmp音声ファイルを作成
    clip_input = mp.VideoFileClip(input_video_path)
    clip_input.audio.write_audiofile(tmp_output_audio_path)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # コーデックは webm にする
    fourcc = cv2.VideoWriter_fourcc(*'webm')
    out = cv2.VideoWriter(tmp_output_video_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        pixelated_frame = pixelate(frame, pixel_size)
        out.write(pixelated_frame)

    cap.release()
    out.release()

    # 音声と動画を結合
    clip = mp.VideoFileClip(tmp_output_video_path).subclip()
    clip.write_videofile(output_video_path, audio=tmp_output_audio_path)

    # tmp フォルダを削除
    shutil.rmtree("./tmp")
    os.mkdir("tmp")


if __name__ == "__main__":
    convert_to_pixel_art( "input_video.mp4", "output_video.mp4", pixel_size=16)
