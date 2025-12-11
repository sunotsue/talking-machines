# 🎙️ Talking Machines by Su Park

An automated podcast creation pipeline that transforms academic AI papers into engaging, conversational podcast episodes — from PDF to audio.

## 🌐 Listen now

* [Spotify](https://open.spotify.com/show/35IuQwu17BwEUC9h24Yn8l?si=5135ad257ecb4683&nd=1&dlsi=99c6dafc50a24054)
* [Apple Podcasts](https://podcasts.apple.com/us/podcast/talking-machines-by-su-park/id1805363038)
* [YouTube](https://www.youtube.com/@talkingmachinespod)

## 🧠 Overview

Talking Machines combines GPT-4 and ElevenLabs text-to-speech to automatically create podcast episodes from academic papers. The pipeline generates natural two-host conversations between Vic and Alex, discussing AI research in an accessible, engaging format.

## ⚙️ Workflow

The pipeline consists of three automated steps:

1. **Script Generation (`generate_script.py`)** — GPT-4o-mini
   * Reads an academic PDF from the `pdfs/` directory
   * Generates a 4-segment conversational script (~2,200 words total)
   * Creates natural dialogue between two distinct hosts (Vic and Alex)
   * Outputs: `scripts/[pdf_name]_[first_speaker]_first.txt`

2. **Metadata Generation (`generate_metadata.py`)** — GPT-4o-mini
   * Analyzes the generated script
   * Creates a catchy episode title and 2-paragraph description
   * Outputs: `metadata/[script_name]_metadata.txt`

3. **Audio Synthesis (`generate_audio.py`)** — ElevenLabs API
   * Converts the script into lifelike audio using two distinct voices
   * Alternates speakers based on script structure
   * Outputs: `audio/[script_name].mp3`

## 🧩 Requirements

* Python 3.10+
* OpenAI API key (GPT-4o-mini access)
* ElevenLabs API key
* Dependencies listed in `requirements.txt`

## 🚀 Setup

### Option 1: Automated Setup (Recommended)
```bash
# 1. Clone the repository
git clone https://github.com/sunotsue/talking-machines.git
cd talking-machines

# 2. Run setup script
chmod +x setup.sh
./setup.sh

# 3. Activate the environment
conda activate talking-machines

# 4. Edit .env with your API keys
nano .env  # or use your preferred editor
```

### Option 2: Manual Setup
```bash
# 1. Clone the repository
git clone https://github.com/sunotsue/talking-machines.git
cd talking-machines

# 2. Create conda environment
conda create -n talking-machines python=3.10 -y
conda activate talking-machines

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create required directories
mkdir -p pdfs scripts metadata audio

# 5. Set up environment variables
cp .env.example .env
# Edit .env with your actual API keys
```

### API Keys Setup

Edit `.env` and replace with your actual keys:
```bash
OPENAI_API_KEY=sk-proj-...
ELEVENLABS_API_KEY=...
```

**Get your API keys:**
* OpenAI: https://platform.openai.com/api-keys
* ElevenLabs: https://elevenlabs.io/app/settings/api-keys

## ▶️ Usage

### Step 1: Prepare Your Paper

Place **one** PDF file in the `pdfs/` directory:
```bash
cp your_paper.pdf pdfs/
```

### Step 2: Generate the Script
```bash
python generate_script.py
```

Output: `scripts/[paper_name]_[Vic|Alex]_first.txt`

### Step 3: Generate Episode Metadata
```bash
python generate_metadata.py
```

Output: `metadata/[paper_name]_metadata.txt`

### Step 4: Generate Audio
```bash
python generate_audio.py
```

Output: `audio/[paper_name].mp3`

## 📦 Output Files

* 📝 **Script**: `scripts/[paper_name]_[first_speaker]_first.txt` — Conversational dialogue between Vic and Alex
* 📋 **Metadata**: `metadata/[paper_name]_metadata.txt` — Episode title and description
* 🎧 **Audio**: `audio/[paper_name].mp3` — Final podcast episode (MP3, 44.1kHz, 128kbps)

## 🎭 Podcast Hosts

* **Vic**: Sharp-witted British host in her early 20s, San Francisco-based, optimistic about AI development with dry humor
* **Alex**: Grounded New York-based host in her early 20s, safety-focused with thoughtful questions and practical perspective

## 🪄 Features

* Automated script segmentation (Introduction, Key Concepts Part 1 & 2, Closing)
* Natural speaker alternation with no manual intervention required
* Professional audio quality using ElevenLabs multilingual v2 voices
* Consistent branding and closing message across episodes

## 📝 Notes

* Each script processes **one** PDF at a time — ensure only one file exists in `pdfs/` directory
* Script generation uses ~3-second delays between segments to avoid rate limits
* Total processing time: ~5-10 minutes per episode (depending on paper length)
* Voice IDs are configurable in `generate_audio.py` if you want different ElevenLabs voices

## 🔒 Security

* **Never commit `.env` to version control** — it contains your API keys
* `.env` is already in `.gitignore` to prevent accidental commits
* Use `.env.example` as a template for required environment variables
