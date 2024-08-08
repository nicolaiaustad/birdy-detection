import cv2
import pandas as pd
from ultralytics import YOLO
import os
import torch

#Function to enable use of GPU if available for faster processing
def get_device():
    return 'cuda' if torch.cuda.is_available() else 'cpu'

# Helper function to extract frame_id from filename
def extract_frame_id(filename):
    return int(filename.split('_')[1].split('.')[0])

    
def detect_objects(frames_path, output_csv):
    
    model = YOLO('yolov8n.pt')
    results = []
    
    # Ensure we read the frames in order
    frame_files = sorted([f for f in os.listdir(frames_path) if f.endswith(".jpg")], key=extract_frame_id)
    
    # Loop through each frame in the frames folder
    for frame_file in frame_files:
        
        if frame_file.endswith(".jpg"):
            
            #Create a path to the frame and read the frame image
            frame_path = os.path.join(frames_path, frame_file)
            frame = cv2.imread(frame_path)
            

            #Make predictions on the frame
            detections = model(frame)
            
            for detection in detections: #There is only one object in detections as we only made predictions on one single frame, but we must still loop through it
                for d in detection.boxes.data.tolist(): #Coverting the tensor to a list
                    x1, y1, x2, y2, score, class_id = d   
                    class_name = model.names[int(class_id)]            
                    timestamp = frame_file.split('_')[-1].split('.')[0] #Split by underscore and then by dot to get the timestamp.
                    frame_id = frame_file.split('_')[1] #Split by underscore to get the frame id.
                    
                    #Optional: Add a "If class_name == 'bird'" statement to only save the bounding box coordinates for birds before appending.
                    #Now we collect all detections in CSV file.
                    
                    results.append({
                        'Class': class_name,
                        'Timestamp': timestamp,
                        'Frame': frame_id,
                        'BoundingBox_Coord_0': x1,
                        'BoundingBox_Coord_1': y1,
                        'BoundingBox_Coord_2': x2,
                        'BoundingBox_Coord_3': y2,
                        'Confidence': score
                    })
            
            
    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)

