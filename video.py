import cv2 
import os
from datetime import timedelta

def format_timestamp(seconds):
    return str(timedelta(seconds=seconds))

def extract_frames(video_path, output_path):
    # Create a directory to store the frames
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Open the video file
    video = cv2.VideoCapture(video_path)
    i = 0
   
    
    while video.isOpened():
        #Read through the video frame by frame
        ret, frame = video.read()
        if not ret:
            break
        
        
        
        # Get the timestamp for the current frame in correct format for CSV file
        timestamp_seconds = round(video.get(cv2.CAP_PROP_POS_MSEC) / 1000.0)  # convert to seconds and round
        timestamp_hhmmss = format_timestamp(timestamp_seconds)
        
        #Give each frame a unique identifier
        #frame_name = f'frame_{i}.jpg'
        
        # Save each frame to disk with a unique name
        cv2.imwrite(f'{output_path}/frame_{i}_'+str(timestamp_hhmmss)+'.jpg', frame)
        
        i += 1

    video.release()

 
