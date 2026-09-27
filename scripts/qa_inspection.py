# -*- coding: utf-8 -*-
"""
tutorial-animation-architect: 自動化抽幀質檢與規格驗證工具 (QA Inspection)
功能：
1. 檢驗 MP4 技術規格（解析度、幀率、音訊取樣率、聲道、檔案大小）
2. 自動抽取九大經典分鏡的關鍵幀 PNG，供排版、文字無重疊、無亂碼驗證
"""

import os
import json
import subprocess

def inspect_video_specs(video_path):
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_format", "-show_streams", video_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, text=True, encoding="utf-8")
    data = json.loads(res.stdout)
    
    info = {}
    for s in data["streams"]:
        if s["codec_type"] == "video":
            info["video_codec"] = s["codec_name"]
            info["resolution"] = f"{s['width']}x{s['height']}"
            info["fps"] = s["r_frame_rate"]
            info["duration_sec"] = float(s.get("duration", 0))
        elif s["codec_type"] == "audio":
            info["audio_codec"] = s["codec_name"]
            info["sample_rate"] = int(s["sample_rate"])
            info["channels"] = int(s["channels"])
            
    fmt = data["format"]
    info["file_size_mb"] = round(float(fmt["size"]) / (1024 * 1024), 2)
    info["bitrate_kbps"] = round(int(fmt["bit_rate"]) / 1000, 1)
    
    print("\n=== MP4 規格檢驗報告 ===")
    for k, v in info.items():
        print(f"  {k}: {v}")
    return info

def extract_qa_frames(video_path, timestamps, output_dir="qa_frames"):
    os.makedirs(output_dir, exist_ok=True)
    extracted = []
    for ts in timestamps:
        out_png = os.path.join(output_dir, f"frame_{int(ts):03d}s.png")
        subprocess.run([
            "ffmpeg", "-y", "-ss", str(ts), "-i", video_path,
            "-vframes", "1", "-q:v", "2", out_png
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        extracted.append(out_png)
        print(f"  Extracted QA frame at {ts}s -> {out_png}")
    return extracted

if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "Excel記帳入門_教學動畫.mp4"
    if os.path.exists(target):
        inspect_video_specs(target)
        extract_qa_frames(target, [5, 17, 36, 52, 71, 88, 104, 118, 138])
    else:
        print(f"File not found: {target}")
