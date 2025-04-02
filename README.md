# talking-machines-pod

An automated podcast creation workflow that leverages AI to generate engaging podcast content and convert it into natural-sounding audio.

## Workflow Overview

### 1. Script Generation (GPT-4o-mini)
- Takes a user-provided prompt and PDF document as input
- Uses GPT-4o-mini model to analyze the content and generate a natural podcast script
- The script is structured for a two-person conversation format
- Ensures engaging and coherent dialogue between hosts

### 2. Audio Generation (ElevenLabs API)
- Converts the generated script into high-quality audio
- Supports two distinct voice IDs for a natural podcast conversation
- Generates an MP3 file with the complete podcast episode
- Maintains natural intonation and conversation flow

## Requirements
- OpenAI API key
- ElevenLabs API key
- Python environment with required dependencies

## Setup
1. Clone the repository
2. Make the setup script executable:
   ```bash
   chmod +x setup.sh
   ```
3. Run the setup script:
   ```bash
   ./setup.sh
   ```
4. Edit the `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
   ```

## Usage
1. Prepare your prompt and PDF document
2. Run the script generation process
3. Review and adjust the generated script if needed
4. Generate the final podcast audio
5. Export the MP3 file

## Output
- Generated podcast script in text format
- Final podcast episode in MP3 format