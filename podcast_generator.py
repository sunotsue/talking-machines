import os
import sys
from dotenv import load_dotenv
from elevenlabs import generate, set_api_key, save, play, Voice, VoiceSettings

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
        set_api_key(api_key)
        
        # Voice IDs for the hosts
        self.voice_ids = {
            "Vic": "pNInz6obpgDQGcFmaJgB",  # British female voice
            "Alex": "ThT5KcBeYPX3keUQqHPh"  # American female voice
        }
        
        # Voice settings for more natural speech
        self.voice_settings = VoiceSettings(
            stability=0.5,
            similarity_boost=0.75,
            style=0.0,
            use_speaker_boost=True
        )
    
    def generate_podcast(self, script_file_path):
        """
        Generate a podcast audio file from a script.
        
        Args:
            script_file_path (str): Path to the script file
            
        Returns:
            str: Path to the generated audio file
        """
        # Determine the first and second speakers based on the filename
        is_vic_first = "Vic_first" in script_file_path
        first_speaker = "Vic" if is_vic_first else "Alex"
        second_speaker = "Alex" if is_vic_first else "Vic"
        
        print(f"First speaker: {first_speaker}")
        print(f"Second speaker: {second_speaker}")
        
        # Read the script file
        with open(script_file_path, 'r', encoding='utf-8') as file:
            script_content = file.read()
        
        # Split the script into segments (each segment is separated by double newlines)
        segments = script_content.split('\n\n')
        
        # Create audio directory if it doesn't exist
        audio_dir = "audio"
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)
        
        # Generate audio for each segment
        audio_segments = []
        for i, segment in enumerate(segments):
            if segment.strip():  # Skip empty segments
                # Determine the speaker for this segment
                speaker = first_speaker if i % 2 == 0 else second_speaker
                voice_id = self.voice_ids[speaker]
                
                print(f"Generating audio for segment {i+1} with {speaker}'s voice...")
                
                # Create a Voice object with the voice ID and settings
                voice = Voice(
                    voice_id=voice_id,
                    settings=self.voice_settings
                )
                
                # Generate audio with the voice object
                audio = generate(text=segment, voice=voice)
                audio_segments.append(audio)
        
        # Combine all audio segments
        combined_audio = b''.join(audio_segments)
        
        # Save the combined audio to a file
        output_filename = os.path.basename(script_file_path).replace('.txt', '.mp3')
        output_path = os.path.join(audio_dir, output_filename)
        save(combined_audio, output_path)
        
        print(f"Podcast generated successfully! Saved to: {output_path}")
        return output_path

def main():
    """Main function to generate a podcast from a script file."""
    generator = PodcastGenerator()
    
    # Get the script file path from command line arguments or use default
    script_file_path = sys.argv[1] if len(sys.argv) > 1 else "scripts/generated_script_chunked_6_Vic_first.txt"
    
    try:
        output_path = generator.generate_podcast(script_file_path)
        print(f"Podcast saved to: {output_path}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 