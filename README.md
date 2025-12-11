# 🎙️ Talking Machines by Su Park

An automated podcast creation pipeline that uses AI to turn written content into natural, engaging podcast episodes — from script to voice.

## 🌐 Listen now

* [Spotify](https://open.spotify.com/show/35IuQwu17BwEUC9h24Yn8l?si=5135ad257ecb4683&nd=1&dlsi=99c6dafc50a24054)
* [Apple Podcasts](https://podcasts.apple.com/us/podcast/talking-machines-by-su-park/id1805363038)
* [YouTube](https://www.youtube.com/@talkingmachinespod)

## 🧠 Overview

Talking Machines combines large language models and realistic text-to-speech to automate the creation of podcast episodes. Given a topic or document, it generates a two-person conversational script and produces a studio-quality MP3.

## ⚙️ Workflow

1. **Script Generation — GPT-4o-mini**
   * Ingests a user prompt and optional PDF document.
   * Analyzes, summarizes, and transforms content into a dialogue-style podcast script.
   * Structures content for two hosts, ensuring tone, pacing, and engagement.

2. **Audio Synthesis — ElevenLabs API**
   * Converts the generated script into lifelike audio.
   * Supports two distinct voices for natural back-and-forth rhythm.
   * Outputs a single MP3 episode with balanced intonation and conversational flow.

## 🧩 Requirements

* OpenAI API key
* ElevenLabs API key
* Python 3.9+ environment with dependencies from `requirements.txt`

## 🚀 Setup
```bash
# 1. Clone the repository
git clone https://github.com/yourusername/talking-machines.git
cd talking-machines

# 2. Make setup script executable
chmod +x setup.sh

# 3. Run setup
./setup.sh

# 4. Configure environment
echo "OPENAI_API_KEY=your_openai_api_key_here" >> .env
echo "ELEVENLABS_API_KEY=your_elevenlabs_api_key_here" >> .env
```

## ▶️ Usage

1. **Prepare inputs**
   * A concise prompt describing your desired topic.
   * An optional PDF document (e.g., paper, report, or essay).

2. **Generate the script**
```bash
python generate_script.py
```

3. **Review the script** (optional edits).

4. **Produce the audio**
```bash
python generate_audio.py
```

5. Find your final MP3 in the `output/` directory.

## 📦 Output

* 📝 `podcast_script.txt` — AI-generated conversational script.
* 🎧 `episode_final.mp3` — Completed podcast episode ready for upload.

## 🪄 Notes

* Customization of voices, pacing, and tone via `config.json` is planned.
* Integrations for episode publishing (e.g., YouTube/Spotify upload) are planned.
