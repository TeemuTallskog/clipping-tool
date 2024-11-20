from moviepy.editor import VideoFileClip, CompositeVideoClip
from moviepy.video.fx.all import crop
from moviepy.video.compositing.concatenate import concatenate_videoclips
from PIL import Image, ImageFilter, ImageEnhance
from numpy import array as np_array
import argparse
import re

COLOR = 1.5
BRIGHTNESS = 1.5
SHARPNESS = 2

def blur(image):
    img = Image.fromarray(image)
    blurred_img = img.filter(ImageFilter.GaussianBlur(radius=15))
    return np_array(blurred_img)

def enhance_frame(frame):
    img = Image.fromarray(frame)

    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(COLOR)

    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(BRIGHTNESS)

    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(SHARPNESS)
    
    return np_array(img)

def split_video(input_file, clips, output_file, short=False):
    try:
        video = VideoFileClip(input_file)
        for start, end in clips:
            if start < 0 or end > video.duration or start >= end:
                raise ValueError("Invalid timestamps. Ensure start < end and within video duration.")
        
        video_parts = [video.subclip(start,end) for start, end in clips]

        trimmed_video = concatenate_videoclips(clips=video_parts)
        trimmed_video = trimmed_video.fl_image(enhance_frame)

        if short:
            video_width, video_height = trimmed_video.size

            target_width = video_height * 9 / 16

            if target_width > video_width:
                raise ValueError("Input video is too narrow for the desired aspect ratio.")

            x_center = video_width / 2
            drop_crop_x1 = x_center - target_width / 2
            drop_crop_x2 = x_center + target_width / 2

            trimmed_backdrop_video = crop(trimmed_video, x1=drop_crop_x1, y1=0, x2=drop_crop_x2, y2=video_height)
            blurred_backdrop = trimmed_backdrop_video.fl_image(blur)
            blurred_backdrop = blurred_backdrop.resize(2)
            trimmed_main_video = crop(trimmed_video, width=video_height, height=video_height, x_center=video_width // 2, y_center=video_height // 2)
            trimmed_main_video = trimmed_main_video.resize(width=blurred_backdrop.w)

            trimmed_video = CompositeVideoClip([blurred_backdrop, trimmed_main_video.set_position("center")])

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
    global COLOR
    global BRIGHTNESS
    global SHARPNESS
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", type=str, required=True)
    parser.add_argument("-c", "--clip", nargs='+', type=time_type, required=True, help="Provide time stamps in format HH:mm:ss-HH:mm:ss. eg. 0:1:22-0:1:30")
    parser.add_argument("-o", "--output", type=str, default="output.mp4")
    parser.add_argument("-yts", "--youtube-short", action="store_true")
    parser.add_argument("-col", "--color", type=float, default=1.5, help="Float, adjust color")
    parser.add_argument("-bri", "--birghtness", type=float, default=1.5, help="Float, adjust brightness")
    parser.add_argument("-sha", "--sharpness", type=float, default=2, help="Float, adjust sharpness")

    args = parser.parse_args()
    input_video = args.path
    clips = args.clip
    output_video = args.output 
    short = args.youtube_short
    COLOR = args.color
    BRIGHTNESS = args.birghtness
    SHARPNESS = args.sharpness

    split_video(input_video, clips, output_video, short)

if __name__ == "__main__":
    main()