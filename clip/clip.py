from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.fx.all import crop
import argparse
import re

def split_video(input_file, start_sec, end_sec, output_file, short=False):
    """
    Splits a video between two timestamps and saves the result.

    Parameters:
        input_file (str): Path to the input video file.
        start_time (str): Start time in "HH:MM:SS" or "MM:SS" format.
        end_time (str): End time in "HH:MM:SS" or "MM:SS" format.
        output_file (str): Path to save the output video.
    """
    try:
        video = VideoFileClip(input_file)
        if start_sec < 0 or end_sec > video.duration or start_sec >= end_sec:
            raise ValueError("Invalid timestamps. Ensure start < end and within video duration.")

        trimmed_video = video.subclip(start_sec, end_sec)

        if short:
            video_width, video_height = trimmed_video.size

            target_width = video_height * 9 / 16

            if target_width > video_width:
                raise ValueError("Input video is too narrow for the desired aspect ratio.")

            x_center = video_width / 2
            crop_x1 = x_center - target_width / 2
            crop_x2 = x_center + target_width / 2

            trimmed_video = crop(trimmed_video, x1=crop_x1, y1=0, x2=crop_x2, y2=video_height)

        trimmed_video.write_videofile(output_file, codec="libx264", audio_codec="aac")

        print(f"Video split successfully! Saved to {output_file}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        video.close()

def time_type(value):
    pattern = r'\d+:\d+:\d+'
    if not re.search(pattern, value):
        raise argparse.ArgumentTypeError(f"Invalid value: {value}")
    parts = list(map(int, value.split(":")))
    return sum(p * 60 ** i for i, p in enumerate(reversed(parts)))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", type=str, required=True)
    parser.add_argument("-s", "--start", type=time_type, required=True)
    parser.add_argument("-e", "--end", type=time_type, required=True)
    parser.add_argument("-o", "--output", type=str, default="output.mp4")
    parser.add_argument("-yts", "--youtube-short", action="store_true")
    args = parser.parse_args()
    input_video = args.path
    start = args.start
    end = args.end 
    output_video = args.output 
    short = args.youtube_short

    split_video(input_video, start, end, output_video, short)

if __name__ == "__main__":
    main()