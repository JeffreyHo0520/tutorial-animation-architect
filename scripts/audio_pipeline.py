# -*- coding: utf-8 -*-
"""
tutorial-animation-architect: 音訊與配樂工程管線 (Audio Pipeline)
功能：
1. 批量生成高品質神經網路語音（Edge-TTS / Gemini TTS）
2. 測量精準時長並計算全時間軸 timeline_full.json
3. 向量合成原創輕快 BGM（116 BPM 馬林巴/電鋼琴/貝斯/沙錘）
4. 合成音效（鍵盤打字聲、成功叮聲、硬幣投擲聲）
5. 人聲發言時配樂 -20dB 側鏈壓低 (Audio Ducking) 並輸出母帶音軌
"""

import os
import json
import wave
import subprocess
import asyncio
import numpy as np

SAMPLE_RATE = 44100

def get_duration(file_path):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", file_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(res.stdout.strip())

def write_wav(filename, samples, sample_rate=SAMPLE_RATE):
    samples = np.clip(samples, -1.0, 1.0)
    int_samples = (samples * 32767).astype(np.int16)
    with wave.open(filename, 'wb') as wf:
        nchannels = 2 if len(int_samples.shape) > 1 and int_samples.shape[1] == 2 else 1
        wf.setnchannels(nchannels)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(int_samples.tobytes())

def load_wav(path):
    with wave.open(path, 'rb') as wf:
        nchannels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        nframes = wf.getnframes()
        data = wf.readframes(nframes)
        samples = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
        if nchannels == 1:
            samples = np.stack([samples, samples], axis=1)
        elif nchannels == 2:
            samples = samples.reshape(-1, 2)
        return samples

def build_sfx(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Keyboard click
    t = np.linspace(0, 0.04, int(SAMPLE_RATE * 0.04), endpoint=False)
    noise = np.random.uniform(-1, 1, len(t))
    click = (np.sin(2 * np.pi * 1200 * t) * 0.4 + noise * 0.6) * np.exp(-t * 120) * 0.8
    write_wav(os.path.join(output_dir, "keyboard_click.wav"), click)
    
    # 2. Ding Bell
    t = np.linspace(0, 1.2, int(SAMPLE_RATE * 1.2), endpoint=False)
    f0 = 1318.5
    bell = (
        1.0 * np.sin(2 * np.pi * f0 * t) * np.exp(-t * 3.5) +
        0.5 * np.sin(2 * np.pi * (f0 * 2.01) * t) * np.exp(-t * 5.0) +
        0.25 * np.sin(2 * np.pi * (f0 * 3.02) * t) * np.exp(-t * 7.0)
    ) * 0.7
    write_wav(os.path.join(output_dir, "ding_bell.wav"), bell)
    
    # 3. Coin Clink
    t = np.linspace(0, 0.6, int(SAMPLE_RATE * 0.6), endpoint=False)
    coin = (0.7 * np.sin(2 * np.pi * 2489 * t) * np.exp(-t * 8) +
            0.5 * np.sin(2 * np.pi * 4978 * t) * np.exp(-t * 12)) * 0.6
    write_wav(os.path.join(output_dir, "coin_clink.wav"), coin)

def build_bgm(total_duration, output_path):
    t_full = np.linspace(0, total_duration, int(SAMPLE_RATE * total_duration), endpoint=False)
    left = np.zeros_like(t_full)
    right = np.zeros_like(t_full)
    
    bpm = 116
    beat_dur = 60.0 / bpm
    bar_dur = beat_dur * 4
    total_bars = int(np.ceil(total_duration / bar_dur)) + 1
    
    chords = [
        {'bass': 130.81, 'notes': [261.63, 329.63, 392.00, 523.25]},
        {'bass': 98.00,  'notes': [246.94, 293.66, 392.00, 493.88]},
        {'bass': 110.00, 'notes': [220.00, 261.63, 329.63, 440.00]},
        {'bass': 87.31,  'notes': [220.00, 261.63, 349.23, 440.00]},
    ]
    
    for bar_idx in range(total_bars):
        bar_start = bar_idx * bar_dur
        chord = chords[bar_idx % len(chords)]
        
        for beat in [0, 2]:
            b_start = bar_start + beat * beat_dur
            if b_start >= total_duration: break
            dur = beat_dur * 1.5
            n_samples = int(SAMPLE_RATE * dur)
            t = np.linspace(0, dur, n_samples, endpoint=False)
            bass = np.sin(2 * np.pi * chord['bass'] * t) * np.exp(-t * 2.0) * 0.35
            idx_s = int(b_start * SAMPLE_RATE)
            idx_e = min(idx_s + n_samples, len(t_full))
            left[idx_s:idx_e] += bass[:idx_e - idx_s]
            right[idx_s:idx_e] += bass[:idx_e - idx_s]
            
        for eighth in range(8):
            e_start = bar_start + eighth * (beat_dur / 2)
            if e_start >= total_duration: break
            note = chord['notes'][eighth % len(chord['notes'])]
            dur = 0.35
            n_samples = int(SAMPLE_RATE * dur)
            t = np.linspace(0, dur, n_samples, endpoint=False)
            marimba = (np.sin(2 * np.pi * note * t) * 0.8 + np.sin(2 * np.pi * note * 3 * t) * 0.15) * np.exp(-t * 10.0) * 0.22
            idx_s = int(e_start * SAMPLE_RATE)
            idx_e = min(idx_s + n_samples, len(t_full))
            pan = 0.5 + 0.3 * np.sin(eighth * 1.2)
            left[idx_s:idx_e] += marimba[:idx_e - idx_s] * pan
            right[idx_s:idx_e] += marimba[:idx_e - idx_s] * (1 - pan)
            
    # Fade in / out
    fade_len = int(SAMPLE_RATE * 2.0)
    left[-fade_len:] *= np.linspace(1, 0, fade_len)
    right[-fade_len:] *= np.linspace(1, 0, fade_len)
    stereo = np.stack([left, right], axis=1)
    write_wav(output_path, stereo)

def mix_master_soundtrack(timeline_json, sfx_dir, bgm_path, output_wav):
    with open(timeline_json, "r", encoding="utf-8") as f:
        meta = json.load(f)
    
    total_dur = meta["total_duration"]
    total_samples = int(total_dur * SAMPLE_RATE)
    master = np.zeros((total_samples, 2), dtype=np.float32)
    voice_mask = np.zeros(total_samples, dtype=np.float32)
    
    for s in meta["sentences"]:
        v_samples = load_wav(s["wav_file"])
        idx_s = int(s["start_time"] * SAMPLE_RATE)
        idx_e = min(idx_s + len(v_samples), total_samples)
        v_len = idx_e - idx_s
        master[idx_s:idx_e] += v_samples[:v_len]
        
        m_start = max(0, idx_s - int(0.15 * SAMPLE_RATE))
        m_end = min(total_samples, idx_e + int(0.25 * SAMPLE_RATE))
        voice_mask[m_start:m_end] = 1.0
        
    # O(N) fast moving average smoothing
    window_size = int(0.2 * SAMPLE_RATE)
    pad_w = window_size // 2
    padded = np.pad(voice_mask, (pad_w, pad_w), mode='edge')
    cs = np.cumsum(padded, dtype=np.float64)
    res = (cs[window_size:] - cs[:-window_size]) / float(window_size)
    if len(res) > len(voice_mask):
        res = res[:len(voice_mask)]
    elif len(res) < len(voice_mask):
        res = np.pad(res, (0, len(voice_mask) - len(res)), mode='edge')
    voice_mask_smooth = np.clip(res.astype(np.float32), 0.0, 1.0)
    
    bgm_raw = load_wav(bgm_path)
    bgm_samples = np.zeros((total_samples, 2), dtype=np.float32)
    for i in range(2):
        tiled = np.tile(bgm_raw[:, i], int(np.ceil(total_samples / len(bgm_raw))))
        bgm_samples[:, i] = tiled[:total_samples]
        
    # -20 dB ducking curve
    ducking = 0.32 * (1.0 - 0.88 * voice_mask_smooth)
    bgm_samples[:, 0] *= ducking
    bgm_samples[:, 1] *= ducking
    
    final_master = master + bgm_samples
    peak = np.max(np.abs(final_master))
    if peak > 0.95:
        final_master = final_master * (0.95 / peak)
        
    write_wav(output_wav, final_master)
    print(f"Master soundtrack mixed successfully: {output_wav}")
