import os
import sys
import re
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

class EpisodeMetadataGenerator:
    """A class to generate episode title and description from a podcast script."""
    
    def __init__(self):
        """Initialize the EpisodeMetadataGenerator with OpenAI API key."""
        # Initialize OpenAI API key
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Set OpenAI API key
        openai.api_key = api_key
        
        # Model to use for generation
        self.model = "gpt-4o-mini"  # You can change this to gpt-3.5-turbo if needed
    
    def extract_first_few_lines(self, script_content, num_lines=10):
        """Extract the first few lines of the script to get context."""
        lines = script_content.split('\n')
        return '\n'.join(lines[:num_lines])
    
    def get_host_names(self, script_content):
        """
        Extract host names from the script.
        
        Args:
            script_content (str): The full script content
            
        Returns:
            list: List of two host names
        """
        # Look for names in the first few lines where they're likely to be introduced
        lines = script_content.split('\n')[:20]  # Check first 20 lines
        names = set()
        
        for line in lines:
            if line.strip().endswith(':'):
                name = line.strip()[:-1]
                if name and name not in names:
                    names.add(name)
                    if len(names) == 2:
                        return list(names)
        
        return ["Vic", "Alex"]  # Default names if not found
    
    def generate_metadata(self, script_file_path):
        """
        Generate episode title and description from a script file.
        
        Args:
            script_file_path (str): Path to the script file
            
        Returns:
            tuple: (title, description)
        """
        # Read script and get host names
        with open(script_file_path, 'r', encoding='utf-8') as file:
            script_content = file.read()
        
        host_names = self.get_host_names(script_content)
        
        # Generate title and description
        title = self._generate_title(script_content, host_names)
        description = self._generate_description(script_content, title, host_names)
        
        return title, description
    
    def _generate_title(self, script_content, host_names):
        """Generate a catchy and informative title for the episode."""
        prompt = f"""
        You are a podcast producer for "Talking Machines by SU PARK" podcast. 
        Based on the following script excerpt, generate a concise, punchy title for this episode.
        The title should be 3-6 words long, be immediately engaging, and capture the essence of the episode.
        Avoid generic phrases and make it specific to the content.
        
        Hosts: {host_names[0]} and {host_names[1]}
        
        Script excerpt:
        {script_content[:1000]}
        
        Title:
        """
        
        response = openai.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a podcast producer creating punchy, memorable titles."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip().replace('"', '').replace("'", "")
    
    def _generate_description(self, script_content, title, host_names):
        """Generate a compelling description for the episode."""
        prompt = f"""
        You are a podcast producer for "Talking Machines by SU PARK" podcast. 
        Based on the following script excerpt and title, generate a clear, concise description in exactly 2 paragraphs.
        Keep it factual and engaging, without promotional language.
        
        First paragraph:
        - State the main topic clearly
        - Explain its significance
        - Use a direct, engaging tone
        
        Second paragraph:
        - Present 2-3 key insights from the discussion
        - Focus on the most interesting findings or implications
        - Keep it concise and factual
        
        Title: {title}
        
        Script excerpt:
        {script_content[:1500]}
        
        Description:
        """
        
        response = openai.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a podcast producer creating concise, factual descriptions without promotional language."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    def save_metadata(self, title, description, output_file=None):
        """
        Save the generated metadata to a file.
        
        Args:
            title (str): Episode title
            description (str): Episode description
            output_file (str, optional): Path to save the metadata. If None, prints to console.
        """
        metadata = f"Title: {title}\n\nDescription:\n{description}"
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(metadata)
            print(f"Metadata saved to: {output_file}")
        else:
            print("\nGenerated Metadata:")
            print("=" * 50)
            print(metadata)
            print("=" * 50)

def main():
    """Main function to generate episode metadata from a script file."""
    generator = EpisodeMetadataGenerator()
    
    # Get the script file path from command line arguments or use default
    script_file_path = sys.argv[1] if len(sys.argv) > 1 else "scripts/generated_script_chunked_Vic_first.txt"
    
    # Determine output file path
    output_file = None
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        # Create metadata directory if it doesn't exist
        metadata_dir = "metadata"
        if not os.path.exists(metadata_dir):
            os.makedirs(metadata_dir)
        
        # Generate output filename based on script filename
        script_basename = os.path.basename(script_file_path)
        output_file = os.path.join(metadata_dir, f"{os.path.splitext(script_basename)[0]}_metadata.txt")
    
    try:
        print(f"Generating metadata for script: {script_file_path}")
        title, description = generator.generate_metadata(script_file_path)
        generator.save_metadata(title, description, output_file)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 