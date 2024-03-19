import cv2
from PIL import Image
import os
import time
import queue

def capture_frames(video_path, frame_queue, queue_condition, interval=2, max_size=250):
    cap = None
    try:
        # Initialize the video capture
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise IOError("Cannot open video")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Finished reading the video or error reading frame.")
                break  # Exit the loop if the video ends or an error occurs

            # Convert the frame to a PIL Image
            pil_img = Image.fromarray(frame[..., ::-1])  # This reorders BGR to RGB

            # Resize the image
            ratio = max_size / max(pil_img.size)
            new_size = tuple([int(x * ratio) for x in pil_img.size])
            resized_img = pil_img.resize(new_size, Image.LANCZOS)

            try:
                with queue_condition:
                    frame_queue.put(resized_img,  timeout=1)
                    print('frame queue', frame_queue.qsize())
                    queue_condition.notify()  # Notify the narrator thread that a new frame is available
            except queue.Full:
                print("Frame queue is full, skipping frame.")
                continue  # Skip this frame if the queue is full"

            # Wait for a certain interval before capturing the next frame
            time.sleep(interval)
    except Exception as e:
        print(f"Error capturing frames: {e}")
    finally:
        if cap is not None:
            cap.release()
        # Signal that capturing is done
        if frame_queue is not None:
            frame_queue.put(None)
