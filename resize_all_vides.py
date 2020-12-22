import os
import subprocess

# Get the video width
print('This script will rescale MP4 files in the directory to the desired width using ffmpeg.')
video_width = input('That is the width you would like? (pixels): ')

# get all the files listed in the working directory
for file in os.listdir(os.getcwd()):
    filename = os.fsdecode(file)
    if filename.endswith('.mp4'):
        filename_clean = filename.split('.')[0]
        print('Working on: ' + filename_clean)
        subprocess.call(['ffmpeg', '-i', filename, '-vf', 'scale='+video_width+':-1', filename_clean + '_'+video_width+'.mp4'])
