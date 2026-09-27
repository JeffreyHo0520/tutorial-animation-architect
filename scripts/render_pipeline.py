# -*- coding: utf-8 -*-
"""
tutorial-animation-architect: 高清輕量動畫渲染引擎管線 (Render Pipeline)
功能：
1. 以 Python PIL 進行 1080p 30fps 向量幾何繪圖
2. 透過 OS Pipe 直接串流至 FFmpeg stdin（零磁碟 I/O、極致快速）
3. 採用 stdout/stderr 導向 DEVNULL，徹底杜絕 Windows OS 管道死鎖掛起問題
4. 預設使用 libx264 veryfast / CRF 21 編碼，產出 < 30 MB 高清輕量 MP4
"""

import os
import sys
import time
import subprocess
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1920
HEIGHT = 1080
FPS = 30

def get_system_font(size, bold=False, english=False):
    path = r"C:\Windows\Fonts\arial.ttf" if english else (
        r"C:\Windows\Fonts\msjhbd.ttc" if bold else r"C:\Windows\Fonts\msjh.ttc"
    )
    return ImageFont.truetype(path, size)

def draw_rounded_rect(draw, bbox, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

def render_video_to_mp4(render_frame_func, total_frames, audio_file, output_mp4, crf="21", preset="veryfast"):
    print(f"Starting Video Render: 1080p, 30fps, {total_frames} frames", flush=True)
    
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-", # Pipe from stdin
        "-i", audio_file,
        "-c:v", "libx264",
        "-preset", preset,
        "-crf", crf,
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        output_mp4
    ]
    
    # DEVNULL prevents deadlock on Windows!
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    start_time = time.time()
    for frame_idx in range(total_frames):
        t = frame_idx / FPS
        img = render_frame_func(t)
        proc.stdin.write(img.tobytes())
        
        if (frame_idx + 1) % 300 == 0 or frame_idx == total_frames - 1:
            elapsed = time.time() - start_time
            fps_speed = (frame_idx + 1) / max(0.001, elapsed)
            pct = ((frame_idx + 1) / total_frames) * 100
            eta = (total_frames - (frame_idx + 1)) / max(0.001, fps_speed)
            print(f"Render progress: {pct:.1f}% ({frame_idx+1}/{total_frames}) | Speed: {fps_speed:.1f} fps | ETA: {eta:.0f}s", flush=True)
            
    proc.stdin.close()
    proc.wait()
    
    total_sec = time.time() - start_time
    print(f"Render finished in {total_sec:.1f}s!", flush=True)
    if os.path.exists(output_mp4):
        size_mb = os.path.getsize(output_mp4) / (1024 * 1024)
        print(f"Output: {output_mp4} ({size_mb:.2f} MB)", flush=True)
        return True
    return False
