from multiprocessing.pool import ThreadPool
from multiprocessing import cpu_count
from typing import Tuple
import time

import cv2
import tqdm
import playsound

def draw_frame(frame_information: Tuple[int, cv2.VideoCapture]):
    order, frame = frame_information
    
    y, x, _ = frame.shape
    frame_str = ''
    pixel_row = 0
    
    for this_y in range(y):
        for this_x in range(x):
            pixel = '@' if frame[this_y, this_x].all() == 0 else ' '
            frame_str += pixel
            
            pixel_row += 1
            if pixel_row == x:
                frame_str += '\n'
                pixel_row = 0
    
    return order, frame_str
    

def generate_frames(video: cv2.VideoCapture):
    success = True
    order = 0
    
    while success:
        success, frame = video.read()
        _, bw_frame = cv2.threshold(frame, 128, 255, cv2.THRESH_BINARY)

        if bw_frame is None:
            break
        
        y, x, _ = bw_frame.shape
        bw_frame = cv2.resize(bw_frame, (x // 4, y // 5))
        
        yield order, bw_frame
        
        order += 1

if __name__ == '__main__':
    
    VIDEO_PATH = './assets/badapple.mp4'
    VIDEO = cv2.VideoCapture(VIDEO_PATH)
    VIDEO_FRAMES_COUNT = int(VIDEO.get(cv2.CAP_PROP_FRAME_COUNT))
    
    
    with ThreadPool(processes=cpu_count()) as pool:
        frames = list(tqdm.tqdm(pool.imap(draw_frame, generate_frames(VIDEO)), total=VIDEO_FRAMES_COUNT))
        pool.close()
        pool.join()
        
    frames = sorted(frames, key=lambda x: x[0])
    
    playsound.playsound('./assets/badapple.mp3', block=False)
    
    FPS = 30
    skip_ticks = 1/(FPS*1.0)
    next_snap = time.time()
    
    for _, frame in frames:
        next_snap += skip_ticks
        sleep_time = next_snap - time.time()
        
        if sleep_time > 0:
            print(frame)
            time.sleep(sleep_time)