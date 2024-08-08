import video
import predictions
import load_to_db
import load_from_db
import os



def main():
    # Extract frames from video and save them to a folder in jpg format
    video.extract_frames('pigeon.mp4', 'frame_folder')

    # Detect objects in frames and save the results to a CSV file
    predictions.detect_objects('frame_folder', 'detected_objects.csv')


    # Load detected objects into PostgreSQL database
    db_name = os.getenv('DB_NAME', 'nicolaibase')
    db_user = os.getenv('DB_USER', 'nicolai')
    db_password = os.getenv('DB_PASSWORD', '1234')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')

    load_to_db.load_csv_to_postgres(
        'detected_objects.csv',
        db_name,
        db_user,
        db_password,
        db_host,
        int(db_port),  # Ensure this is converted to an integer
        'detections'
    )

    # Load only bird data from the database and plot the highest number of birds detected per second
    load_from_db.load_birds(
        db_name,
        db_user,
        db_password,
        db_host,
        int(db_port),  # Ensure this is converted to an integer
        'detections',
        "birds_plot.png"
    )

if __name__ == "__main__":
    main()