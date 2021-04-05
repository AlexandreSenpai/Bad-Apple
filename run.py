from multiprocessing.pool import ThreadPool
from multiprocessing import cpu_count
from typing import Tuple
import time

import tqdm
import cv2
import playsound


def draw_frame(frame_information: Tuple[int, cv2.VideoCapture]) -> Tuple[int, str]:
    order, frame = frame_information
    
    y, x, z = frame.shape
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

def generate_frames(video_path: str) -> Tuple[int, cv2.VideoCapture]:
    
    video = cv2.VideoCapture(video_path)
    success = True
    order = 0
    
    while success: 
        success, image = video.read()
        _, im_bw = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)
        
        if im_bw is None:
            break
        
        y, x, z = im_bw.shape
        im_bw = cv2.resize(im_bw, (x // 5, y // 5))
        
        yield order, im_bw
        
        order += 1
    

if __name__ == '__main__':
    
    VIDEO_PATH = './assets/badapple.mp4'
    VIDEO = cv2.VideoCapture(VIDEO_PATH)
    VIDEO_FRAMES_COUNT = int(VIDEO.get(cv2.CAP_PROP_FRAME_COUNT))
    del VIDEO
    
    with ThreadPool(processes=cpu_count()) as pool:
        frames = list(tqdm.tqdm(pool.imap(draw_frame, generate_frames(VIDEO_PATH)), total=VIDEO_FRAMES_COUNT))
        pool.close()
        pool.join()
        
    sort = sorted(frames, key=lambda obj: obj[0])
    
    playsound.playsound(r'./assets/badapple.mp3', False)
    
    START = time.time()
    FPS = 30
    skip_ticks = 1/(FPS*1.0)
    i = 0
    next_snap = time.time()
    
    for order, frame in sort:
        time.time()
        i=i+1
        next_snap += skip_ticks
        sleep_time = next_snap-time.time()
        if (sleep_time>0):
            print(frame)
            time.sleep(sleep_time)
