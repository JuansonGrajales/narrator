import os
import queue
import threading
from capture import capture_frames
from narrator import narrate_frame


def main():
    video_path = os.path.join(os.getcwd(), 'video/test.mp4')
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"The specified video path does not exist: {video_path}")  
    
    # Queue for passing frames between capture and narration
    frame_queue = queue.Queue(maxsize=20) # maxsize is optional but can help control memory usage
    queue_condition = threading.Condition()

    def process_frames():
        print('Narration thread started')
        while True:
            with queue_condition:
                while frame_queue.empty():
                    print('queue is empty, waiting for frames...')
                    queue_condition.wait()
                frame = frame_queue.get()
                if frame is None:
                    print('Queue is empty, waiting for frames...')
                    break
                queue_condition.notify()
            print('Processing frame....')
            narrate_frame(frame)

    # Thread for capturing frames
    capture_thread = threading.Thread(target=capture_frames, args=(video_path, frame_queue, queue_condition))

    # Thread for narrating frames
    narrate_thread = threading.Thread(target=process_frames, args=())

    capture_thread.start()
    narrate_thread.start()

    # Wait for the capture thread to finish
    capture_thread.join()
    # Signal the end of capturing to the narrate thread
    frame_queue.put(None)
    # Wait for the narrate thread to finish
    narrate_thread.join()

if __name__ == "__main__":
    main()