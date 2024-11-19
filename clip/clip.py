from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.fx.all import crop
from moviepy.video.compositing.concatenate import concatenate_videoclips
import argparse
import re

def split_video(input_file, clips, output_file, short=False):
    try:
        video = VideoFileClip(input_file)
        for start, end in clips:
            if start < 0 or end > video.duration or start >= end:
                raise ValueError("Invalid timestamps. Ensure start < end and within video duration.")
        
        video_parts = [video.subclip(start,end) for start, end in clips]

        trimmed_video = concatenate_videoclips(clips=video_parts)

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
    pattern = r'\d+:\d+:\d+\-\d+:\d+:\d'
    if not re.search(pattern, value):
        raise argparse.ArgumentTypeError(f"Invalid value: {value}")
    def get_time_in_seconds(stamp):
        parts = list(map(int, stamp.split(":")))
        return sum(p * 60 ** i for i, p in enumerate(reversed(parts)))
    start_end = value.split("-", 1)
    start = get_time_in_seconds(start_end[0])
    end = get_time_in_seconds(start_end[1])
    return (start, end)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", type=str, required=True)
    parser.add_argument("-c", "--clip", nargs='+', type=time_type, required=True, help="Provide time stamps in format HH:mm:ss-HH:mm:ss. eg. 0:1:22-0:1:30")
    parser.add_argument("-o", "--output", type=str, default="output.mp4")
    parser.add_argument("-yts", "--youtube-short", action="store_true")
    args = parser.parse_args()
    input_video = args.path
    clips = args.clip
    output_video = args.output 
    short = args.youtube_short

    split_video(input_video, clips, output_video, short)

if __name__ == "__main__":
    main()