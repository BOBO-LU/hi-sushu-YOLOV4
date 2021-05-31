import os
import re
import sys
import subprocess
from decimal import Decimal

path_of_video_file = "/home/oplabsushi/Desktop/bobo/darknet/hi-sushi/video/GH010006.MP4"
process = subprocess.Popen(['ffmpeg', '-i', path_of_video_file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
stdout, stderr = process.communicate()
matches = re.search(r"Duration:\s{1}(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),", stdout, re.DOTALL).groupdict()
total_sec=(Decimal(matches['hours'])*60*60)+(Decimal(matches['minutes'])*60)+(Decimal(matches['seconds']))    #duration of the media file

dir_name=path_of_video_file.split('.')[0]+"_chunks"
if not os.path.exists(dir_name):                 
    os.makedirs(dir_name)       #creating directory to save the chunks of the media file

from_time=0
file_no=1
file_names=path_of_video_file.split('.')[0]+'_'
while total_sec>0:
    os.system('ffmpeg -ss '+str(from_time)+' -t 600 -i '+path_of_video_file+' '+dir_name+'/'+file_names+str(file_no)+'.mp4')   #In case if you want the chunks of the file to be in other formats then you can change 'mp4' to the required audio or video format.
    file_no=file_no+1
    from_time=from_time+600
    total_sec=total_sec-600