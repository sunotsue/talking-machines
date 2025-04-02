import os
from dotenv import load_dotenv
from elevenlabs import generate, set_api_key, Voice, VoiceSettings
from elevenlabs.api import History

# Load environment variables
load_dotenv()

class PodcastGenerator:
    def __init__(self):
        # Initialize with API key
        api_key = os.getenv('ELEVENLABS_API_KEY')
        if not api_key:
            raise ValueError("ELEVENLABS_API_KEY not found in environment variables")
        set_api_key(api_key)
        
        # Default voice settings
        self.voice_settings = VoiceSettings(
            stability=0.5,
            similarity_boost=0.75,
            style=0.0,
            use_speaker_boost=True
        )

    def generate_podcast(self, script, voice_id_1, voice_id_2, output_path="podcast.mp3"):
        """
        Generate a podcast from a script using two different voices.
        
        Args:
            script (str): The podcast script
            voice_id_1 (str): ElevenLabs voice ID for the first speaker
            voice_id_2 (str): ElevenLabs voice ID for the second speaker
            output_path (str): Path where the final MP3 will be saved
        """
        # Split script into segments for each speaker
        # This is a simple implementation - you might want to make this more sophisticated
        segments = script.split("\n\n")
        
        # Generate audio for each segment
        audio_segments = []
        for i, segment in enumerate(segments):
            if not segment.strip():
                continue
                
            # Alternate between voices
            voice_id = voice_id_1 if i % 2 == 0 else voice_id_2
            
            # Generate audio for this segment
            audio = generate(
                text=segment,
                voice=Voice(
                    voice_id=voice_id,
                    settings=self.voice_settings
                )
            )
            audio_segments.append(audio)
        
        # Combine all audio segments
        final_audio = b"".join(audio_segments)
        
        # Save the final audio file
        with open(output_path, "wb") as f:
            f.write(final_audio)
            
        return output_path

def main():
    # Example usage
    generator = PodcastGenerator()
    
    # Example script (replace with your actual script)
    example_script = """
    Host 1: Welcome to our podcast! Today we're discussing artificial intelligence.
    
    Host 2: Yes, it's an exciting topic. What aspects should we focus on?
    
    Host 1: Let's start with the basics of machine learning.
    """
    
    # Replace these with your actual voice IDs from ElevenLabs
    voice_id_1 = "YOUR_FIRST_VOICE_ID"
    voice_id_2 = "YOUR_SECOND_VOICE_ID"
    
    try:
        output_file = generator.generate_podcast(
            script=example_script,
            voice_id_1=voice_id_1,
            voice_id_2=voice_id_2
        )
        print(f"Podcast generated successfully! Saved to: {output_file}")
    except Exception as e:
        print(f"Error generating podcast: {str(e)}")

if __name__ == "__main__":
    main() 