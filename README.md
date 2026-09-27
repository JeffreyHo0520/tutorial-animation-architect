# 教學動畫與實作範本架構師 (Tutorial Animation & Project Deliverable Architect)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Antigravity](https://img.shields.io/badge/Antigravity-Skill-emerald.svg)](https://github.com/JeffreyHo0520)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-red.svg)](https://ffmpeg.org/)

專為軟體教學、辦公工具（Excel/Notion/Python 等）、科普理財與零基礎新手設計的 **1080p 30fps 輕量級教學動畫** 與 **隨附實作範本** 一條龍自動化製作全域技能。

整合數學與邏輯嚴謹校驗、台灣口語雙語腳本、神經語音合成（TTS）、-20dB 人聲側鏈避讓原創配樂與同步音效、Python PIL 零 I/O 直串 FFmpeg 高清動畫渲染引擎、隨附實作範本檔（.xlsx/.code）生成、以及全流程抽幀檢查機制。

---

## 🌟 核心特色 (Core Features)

1. **數字與範本 100% 同步 (Single Source of Truth)**：
   * 從一開始建立底層資料模型，保證畫面、旁白口播、公式計算與實作範本檔（如 `.xlsx`）數值嚴絲合縫。
2. **親切活潑主持人口播文案**：
   * 專門優化台灣生活與職場口語表達、公式諧音好唸口訣、每句嚴格控制在 35 字以內，並附簡練地道中英對照字幕（杜絕豆腐塊亂碼）。
3. **專業聲學混音工程 (Audio Pipeline)**：
   * 神經網路語音合成（Edge-TTS `zh-TW-HsiaoChenNeural` / Gemini TTS）、鍵盤打字聲、扭力校驗叮聲、原創節奏配樂（116 BPM），並嚴格實施「人聲說話期間配樂自動壓低 -20 dB」側鏈避讓（Audio Ducking）。
4. **極致輕量高清渲染引擎 (Zero Disk I/O & Scene Cache)**：
   * 基於 Python PIL 幾何繪圖直串 FFmpeg 管道，免安裝龐大 AE 軟體。透過場景快取技術，每秒渲染高達 15~20 幀，145~175 秒 1080p 30fps 動畫僅需約 3~4 分鐘完工，檔案嚴格小於 30 MB。
5. **全流程自動化抽幀質檢 (QA Checkpoints)**：
   * 內建全流程關鍵節點幀自動抽取工具，自動驗證開場、步驟、加總、圖表、防呆機制與收尾排版無文字遮擋、字符亂碼與影音精確對位。

---

## 🚀 一鍵跨電腦安裝 (Quick Install)

在任何已配置 Antigravity / Claude Code / Gemini CLI 的 Windows 電腦上，開啟 PowerShell 執行：

```powershell
iex (irm https://raw.githubusercontent.com/JeffreyHo0520/tutorial-animation-architect/main/install.ps1)
```

安裝腳本會自動將技能部署至全域目錄：
`%USERPROFILE%\.gemini\config\skills\tutorial-animation-architect\`

---

## 🛠️ 標準六階段作業工作流 (6-Stage Pipeline)

```
交付成果標準架構/
├── [主題]_教學動畫.mp4       ← 1080p 30fps 輕量高清動畫（約 2~3 分鐘，< 30 MB，可直接下載秒播）
├── [主題]_示範範本.xlsx      ← 隨附實作檔案（含下拉選單、彩色標籤、動態公式與原生圖表）
├── animation_assets/        ← 音訊工程資產（語音分段、原創 BGM、SFX、母帶音軌）
└── final_inspection_frames/ ← 抽幀質檢快照（開場、步驟、加總、圖表、習慣、收尾）
```

* **階段一：底層資料模型設計與數學嚴謹驗證**：建立 6~10 筆生活化具代表性數據與公式。
* **階段二：腳本撰寫與口訣化口播設計（先呈報確認）**：20~22 句、單句繁中 ≤ 35 字、中英對照、口訣化。
* **階段三：語音合成與專業聲學混音 (Audio Pipeline)**：Edge-TTS 逐句合成、精確時長測量、原創 BGM 合成與 -20dB 側鏈混音。
* **階段四：高清輕量動畫渲染引擎 (Render Pipeline)**：PIL 零磁碟 I/O 直串 FFmpeg stdin、Scene Cache 加速、輸出 < 30 MB MP4。
* **階段五：同款可下載 Excel 範本建立 (Companion Deliverable)**：自動使用 openpyxl 建立帶有條件格式、下拉驗證與公式之點檢/記帳簿。
* **階段六：自動化抽幀質檢與交付確認 (QA Checkpoints)**：關鍵時間點抽幀驗證無豆腐塊、排版舒適與影音同步。

---

## 💻 內建工具腳本 (Bundled Scripts)

* `scripts/audio_pipeline.py`：語音生成、時間軸中繼資料分析、原創配樂合成、-20dB 側鏈壓低混音。
* `scripts/render_pipeline.py`：1080p 30fps 深色軟體教學動畫渲染引擎，直串 FFmpeg 管道，自帶九大經典分鏡範本。
* `scripts/qa_inspection.py`：自動化影片規格檢驗與關鍵時間點自動抽幀質檢工具。

---

## 📄 授權條款 (License)

本專案採用 [MIT License](LICENSE) 開源授權。
由 [Jeffrey Ho (何思齊)](https://github.com/JeffreyHo0520) 維護與開發。
