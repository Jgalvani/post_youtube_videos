import argparse
from datetime import datetime

# Command line options
parser = argparse.ArgumentParser(prog='post_youtube_videos', description='Post videos on youtube')
parser.add_argument('-i', '--inputs', type=str, help='video file directories', required=True)
parser.add_argument('-d', '--date', type=lambda s: datetime.strptime(s, '%Y-%m-%d'), help='date to release the first video', required=True)
parser.add_argument('-u', '--unique',  action='store_true', required=False, help='Only post a video for the files in root directory')
args = parser.parse_args()