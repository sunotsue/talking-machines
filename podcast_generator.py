import os
import sys
from dotenv import load_dotenv
from elevenlabs import ElevenLabs, play, save

# Load environment variables
load_dotenv()

class PodcastGenerator:
    """A class to generate podcast audio from a script using ElevenLabs voices."""
    
    def __init__(self):
        """Initialize the PodcastGenerator with ElevenLabs API key and voice IDs."""
        # Initialize ElevenLabs API key
        api_key = os.getenv('ELEVENLABS_API_KEY')
        if not api_key:
            raise ValueError("ELEVENLABS_API_KEY not found in environment variables")
        
        # Initialize ElevenLabs client with API key
        self.client = ElevenLabs(api_key=api_key)
        
        # Voice IDs for the hosts
        self.voice_ids = {
            "Vic": "gmv0PPPs8m6FEf03PImj",  # British female voice
            "Alex": "aEO01A4wXwd1O8GPgGlF"  # American female voice
        }
        
        # Model ID for text-to-speech
        self.model_id = "eleven_multilingual_v2"
        
        # Output format
        self.output_format = "mp3_44100_128"
        
        # Print available voices for debugging
        self.print_available_voices()
    
    def print_available_voices(self):
        """Print all available voices from ElevenLabs API."""
        try:
            available_voices = self.client.voices.get_all()
            print("\nAvailable voices:")
            for voice in available_voices:
                if hasattr(voice, 'name'):
                    print(f"Name: {voice.name}, ID: {voice.voice_id}")
                else:
                    print(f"Voice ID: {voice[0]}")
        except Exception as e:
            print(f"Error fetching voices: {e}")
    
    def generate_audio_segment(self, text, voice_id):
        """
        Generate audio for a single segment of text.
        
        Args:
            text (str): Text to convert to speech
            voice_id (str): Voice ID to use
            
        Returns:
            bytes: Generated audio data
        """
        try:
            audio_generator = self.client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id=self.model_id,
                output_format=self.output_format
            )
            return b''.join(chunk for chunk in audio_generator)
        except Exception as e:
            print(f"Error generating audio: {e}")
            return b''

    def generate_podcast(self, script_file_path):
        """
        Generate a podcast audio file from a script.
        
        Args:
            script_file_path (str): Path to the script file
            
        Returns:
            str: Path to the generated audio file
        """
        # Determine speakers based on filename
        is_vic_first = "Vic_first" in script_file_path
        first_speaker = "Vic" if is_vic_first else "Alex"
        second_speaker = "Alex" if is_vic_first else "Vic"
        
        print(f"First speaker: {first_speaker}")
        print(f"Second speaker: {second_speaker}")
        
        # Read and split script
        with open(script_file_path, 'r', encoding='utf-8') as file:
            segments = [s.strip() for s in file.read().split('\n\n') if s.strip()]
        
        # Create audio directory
        os.makedirs("audio", exist_ok=True)
        
        # Generate audio for each segment
        audio_segments = []
        for i, segment in enumerate(segments):
            speaker = first_speaker if i % 2 == 0 else second_speaker
            print(f"Generating audio for segment {i+1} with {speaker}'s voice...")
            
            audio_data = self.generate_audio_segment(segment, self.voice_ids[speaker])
            if audio_data:
                audio_segments.append(audio_data)
        
        if not audio_segments:
            raise ValueError("No audio segments were generated successfully")
        
        # Combine and save audio
        combined_audio = b''.join(audio_segments)
        output_filename = os.path.basename(script_file_path).replace('.txt', '.mp3')
        output_path = os.path.join("audio", output_filename)
        save(combined_audio, output_path)
        
        print(f"Podcast generated successfully! Saved to: {output_path}")
        return output_path

def main():
    """Main function to generate a podcast from a script file."""
    generator = PodcastGenerator()
    
    # Find the only script file in the scripts directory
    script_dir = "scripts"
    if not os.path.exists(script_dir):
        print(f"Error: Directory '{script_dir}' not found.")
        return
    
    script_files = [f for f in os.listdir(script_dir) if f.endswith('.txt')]
    
    if not script_files:
        print(f"Error: No script files found in '{script_dir}' directory.")
        return
    
    if len(script_files) > 1:
        print(f"Error: Multiple script files found in '{script_dir}' directory. Please ensure only one script file is present.")
        return
    
    script_file_path = os.path.join(script_dir, script_files[0])
    print(f"Using script file: {script_file_path}")
    
    try:
        output_path = generator.generate_podcast(script_file_path)
        print(f"Podcast saved to: {output_path}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
