import os
import time
from dotenv import load_dotenv
from openai import OpenAI
from PyPDF2 import PdfReader
import random

# Load environment variables
load_dotenv()

class ScriptGenerator:
    """A class to generate podcast scripts from academic papers using GPT-4."""
    
    def __init__(self):
        """Initialize the ScriptGenerator with OpenAI client and system prompt."""
        # Initialize OpenAI client
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=api_key)
        
        # System prompt for GPT-4
        self.system_prompt = """You are a professional podcast script writer for "Talking Machines by Su Park", a podcast specifically designed for women aged 15-35 who are curious about AI and technology.

        Host Details:
        - Vic: British, early 20's, sarcastic, witty, and intellectually sharp. She lives in SF but is from London. She's tech-savvy and generally optimistic about AI development. She's quick with clever quips and dry humor, often making witty observations about implementation details and technical choices. She's passionate about making technical concepts accessible and gets excited about clever algorithmic solutions and engineering decisions.
        - Alex: American, early 20's, girl-next-door vibe with a sharp mind. She lives in NY and brings a fresh perspective to technical discussions. She's naturally curious about how things work under the hood and asks insightful questions about methodology and implementation. She has a knack for finding relatable examples to explain complex technical concepts. She's particularly interested in practical applications and real-world performance.

        Conversation Dynamic:
        - Both hosts are capable of being either the explainer or the questioner
        - The explainer dives deep into technical implementation, methodology, and results
        - The questioner asks for clarification on technical details, implementation choices, and experimental design
        - Roles can alternate naturally based on who has more expertise in the specific technical aspect
        - Both maintain their distinct personalities while working together to explain the paper
        - The conversation should feel like two engineers discussing an interesting technical solution
        - Use analogies sparingly and only when they genuinely help explain a technical concept
        - Focus on methodology, implementation details, and experimental results
        - Allow each host to speak for longer stretches when explaining technical concepts
        - Don't switch speakers unnecessarily - let the natural flow of technical discussion determine when to switch
        - Never end segments with goodbyes or wrap-ups unless it's the final closing segment
        - IMPORTANT: Keep the conversation focused on technical details, methodology, and results. While the hosts can briefly mention broader implications, the core discussion should be about how the technology works.

        Script Requirements:
        - Keep the tone conversational but technically sophisticated
        - Use playful banter and natural dialogue flow while maintaining technical depth
        - The audience and the hosts are in their 20's. Do not sound overly formal, but maintain technical rigor
        - Let the natural flow of technical discussion determine who explains and who asks questions
        - Cover key technical details of the paper while maintaining intellectual rigor
        - No citations or music cues
        - Make the dialogue feel lively and engaging while staying technically focused
        - Each segment (except closing) should end mid-conversation about a technical point
        - Avoid artificial transitions or segment markers in the dialogue
        - Focus primarily on methodology, implementation, and results rather than broader implications
        - End segments naturally with technical questions or observations

        Fun and Engagement Requirements:
        - Include observations about clever technical solutions and implementation choices
        - Add relatable technical examples that resonate with a tech-savvy audience
        - Use natural reactions to technical revelations ("oh, that's clever!", "interesting approach!")
        - Include gentle teasing about technical preferences or implementation choices
        - Share moments of technical insight or "aha" moments about the methodology
        - Make witty observations about the technical approaches and design decisions
        - Use casual, modern language while maintaining technical depth
        - Add personality through genuine interest in technical details
        - Keep humor organic and related to technical content
        - Balance fun elements with serious technical discussion
        - Let Vic's excitement about clever solutions and Alex's curiosity about implementation details drive the conversation

        Format Requirements:
        - Write each line of dialogue on its own line
        - Include a blank line between speakers
        - Do not use speaker labels like 'Vic:' or 'Alex:'
        - Keep the formatting clean and consistent throughout

        The script should flow naturally between hosts, with Vic and Alex creating an engaging dynamic throughout the discussion. Make sure the content is both technically rigorous and entertaining, perfect for listening during a commute, workout, or casual walk."""

        # Define segments and their descriptions
        self.segments = {
            "Introduction & Setup": {
                "words": 200,
                "description": "Introduce the podcast and the hosts, establish the context for the discussion of the paper, and set expectations for the depth of discussion to follow."
            },
            "Key Concepts Part 1": {
                "words": 700,
                "description": "Explore the paper's introduction, background, and initial concepts through natural conversation. Focus on clear explanations first, using analogies only when they genuinely help clarify complex concepts. End mid-conversation, ready to flow into the next segment."
            },
            "Key Concepts Part 2": {
                "words": 700,
                "description": "Continue the discussion of the paper's findings and implications, maintaining the natural flow of conversation. Prioritize direct explanations over analogies, using analogies only when they add genuine value to understanding. End mid-conversation, ready to flow into the next segment."
            },
            "Closing": {
                "words": 200,
                "description": "Summarize key points, highlight the most important takeaways, and provide a cohesive wrap-up that encourages reflection and continued curiosity."
            }
        }

    def extract_text_from_pdf(self, pdf_path):
        """
        Extract text content from a PDF file.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            str: Extracted text content from the PDF
        """
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    def extract_last_words(self, text, num_words=200):
        """
        Extract the last N words to provide context continuity.
        
        Args:
            text (str): The text to extract from
            num_words (int): Number of words to extract
            
        Returns:
            str: The last N words of the text
        """
        words = text.split()
        if len(words) <= num_words:
            return text
        return ' '.join(words[-num_words:])

    def extract_topic_from_filename(self, pdf_path):
        """
        Extract the topic from the PDF filename.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            str: The extracted topic from the filename
        """
        # Get just the filename without extension and directory
        filename = os.path.basename(pdf_path)
        # Remove the .pdf extension
        filename = os.path.splitext(filename)[0]
        # Remove any numbers and special characters at the start
        filename = ''.join(c for c in filename if not c.isdigit() and c not in '.()')
        # Remove any extra spaces and underscores
        filename = filename.strip().replace('_', ' ')
        return filename

    def split_pdf_content(self, pdf_content):
        """
        Split the PDF content into two roughly equal parts.
        
        Args:
            pdf_content (str): The full PDF content
            
        Returns:
            tuple: (first_half, second_half) of the PDF content
        """
        # Split the content into paragraphs
        paragraphs = pdf_content.split('\n\n')
        
        # Calculate the midpoint
        mid_point = len(paragraphs) // 2
        
        # Split into first and second half
        first_half = '\n\n'.join(paragraphs[:mid_point])
        second_half = '\n\n'.join(paragraphs[mid_point:])
        
        return first_half, second_half

    def generate_segment(self, segment_name, word_count, pdf_content, conversation_history="", pdf_path=""):
        """
        Generate a specific segment of the podcast script.
        
        Args:
            segment_name (str): Name of the segment to generate
            word_count (int): Target word count for the segment
            pdf_content (str): Content of the PDF
            conversation_history (str): Previous conversation for context
            pdf_path (str): Path to the PDF file
            
        Returns:
            str: Generated segment content
        """
        segment_info = self.segments[segment_name]
        
        if segment_name == "Introduction & Setup":
            # Randomly select the first speaker
            first_speaker = random.choice(["Vic", "Alex"])
            second_speaker = "Alex" if first_speaker == "Vic" else "Vic"
            
            user_message = f"""Write a lively, engaging introduction to the podcast. Include:
            1. The exact intro line combined with host introductions in a single line. Here's an example: "Welcome to 'Talking Machines by Su Park' the podcast where we talk machines, the bots, and the hottest AI papers off the press, to demystify the world of artificial intelligence research!!! I'm {first_speaker}, and with me today is my lovely co-host, {second_speaker}."
            2. Then, focus on the main thesis of the paper. Extract the key argument or main point from the PDF content and present it in an engaging way.
            3. Keep the tone sophisticated yet engaging, and maintain the natural flow between hosts.
            4. End mid-conversation, ready to flow into the next segment.
            5. IMPORTANT: Do not have the hosts read off or describe their own character traits or backgrounds. They should not mention their accents, where they're from, or their personality traits. Just have them introduce themselves by name only.
            
            PDF Content:
            {pdf_content}
            
            Format the dialogue naturally, without using speaker labels like 'Vic:' or 'Alex:'. Instead, write each line of dialogue on its own line with a blank line between speakers.
            
            Ensure the flow feels natural and engaging."""
        elif segment_name == "Key Concepts Part 1":
            # Get first half of the paper
            first_half, _ = self.split_pdf_content(pdf_content)
            user_message = f"""Continue the podcast script from the previous segment. The conversation so far is:
            {conversation_history}

            Segment Description: {segment_info['description']}
            Target Word Count: {word_count}

            PDF Content:
            {first_half}

            Write approximately {word_count} words, continuing the natural conversation about the paper.
            Specifically:
            1. Continue the discussion naturally without any meta-commentary about transitions or segments
            2. Cover the paper's introduction, background, and key concepts
            3. End mid-conversation, ready to flow into the next segment
            4. Do not use phrases like "let's pick up where we left off" or any other meta-commentary about the conversation flow
            5. Allow each host to speak for longer stretches when explaining concepts
            6. Do not switch speakers unnecessarily - let the natural flow of ideas determine when to switch
            7. IMPORTANT: Do not have the hosts read off or describe their own character traits or backgrounds. They should not mention their accents, where they're from, or their personality traits.
            
            Include sophisticated banter, back-and-forth discussion, and lively conversation.
            Break down complex concepts into clear, professional explanations with natural dialogue flow.
            Ensure the conversation between Vic and Alex remains balanced and engaging throughout.
            
            Format the dialogue naturally, without using speaker labels like 'Vic:' or 'Alex:'. Instead, write each line of dialogue on its own line with a blank line between speakers.
            
            Ensure the flow feels natural and engaging."""
        elif segment_name == "Key Concepts Part 2":
            # Get second half of the paper
            _, second_half = self.split_pdf_content(pdf_content)
            user_message = f"""Continue the podcast script from the previous segment. The conversation so far is:
            {conversation_history}

            Segment Description: {segment_info['description']}
            Target Word Count: {word_count}

            PDF Content:
            {second_half}

            Write approximately {word_count} words, continuing the natural conversation about the paper.
            Specifically:
            1. Continue the discussion naturally without any meta-commentary about transitions or segments
            2. Cover the remaining concepts, findings, and implications
            3. End mid-conversation, ready to flow into the next segment
            4. Do not use phrases like "let's pick up where we left off" or any other meta-commentary about the conversation flow
            5. Allow each host to speak for longer stretches when explaining concepts
            6. Do not switch speakers unnecessarily - let the natural flow of ideas determine when to switch
            7. IMPORTANT: Do not have the hosts read off or describe their own character traits or backgrounds. They should not mention their accents, where they're from, or their personality traits.
            
            Include sophisticated banter, back-and-forth discussion, and lively conversation.
            Break down complex concepts into clear explanations with natural dialogue flow.
            Ensure the conversation between Vic and Alex remains balanced and engaging throughout.
            
            Format the dialogue naturally, without using speaker labels like 'Vic:' or 'Alex:'. Instead, write each line of dialogue on its own line with a blank line between speakers.
            
            Ensure the flow feels natural and engaging."""
        elif segment_name == "Closing":
            # Extract topic from PDF filename
            topic = self.extract_topic_from_filename(pdf_path)
            user_message = f"""Continue the podcast script from the previous segment. The conversation so far is:
            {conversation_history}

            Segment Description: {segment_info['description']}
            Target Word Count: {word_count}

            PDF Content:
            {pdf_content}

            Write approximately {word_count} words, ensuring the dialogue transitions smoothly into the closing message. 
            Include sophisticated banter, back-and-forth discussion, and lively conversation.
            Break down complex concepts into clear, professional explanations with natural dialogue flow.
            Ensure the conversation between Vic and Alex remains balanced and engaging throughout.
            
            End with this exact closing message:
            "Thanks for joining us on Talking Machines today! We hope you enjoyed learning about {topic}. Our goal is not to bore you but fill you in on what's happening in the sci-fi-slowly-becoming-our-reality era we're living in. And today we learned about {topic}.
            Until next time! You can find us on instagram at talking underscore machines underscore podcast."
            
            IMPORTANT: Do not have the hosts read off or describe their own character traits or backgrounds. They should not mention their accents, where they're from, or their personality traits.
            
            Format the dialogue naturally, without using speaker labels like 'Vic:' or 'Alex:'. Instead, write each line of dialogue on its own line with a blank line between speakers.
            
            Ensure the flow feels natural and engaging."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=3000,
                temperature=0.7,
                top_p=0.9
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating segment '{segment_name}': {e}")
            return ""

    def clean_filename(self, filename):
        """
        Clean a filename by removing extension and special characters.
        
        Args:
            filename (str): Original filename
            
        Returns:
            str: Cleaned filename
        """
        # Remove extension and clean up
        name = filename.replace('.pdf', '')
        # Keep only alphanumeric characters and spaces
        name = ''.join(c for c in name if c.isalnum() or c.isspace())
        # Replace spaces with underscores
        return name.replace(' ', '_')

    def generate_full_script(self, pdf_path):
        """
        Generate the complete podcast script in segments.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            tuple: (complete_script, output_path)
        """
        # Extract text from PDF
        pdf_content = self.extract_text_from_pdf(pdf_path)
        
        # Store the complete script and conversation history
        complete_script = ""
        conversation_history = ""
        
        # Generate each segment
        for segment_name, info in self.segments.items():
            print(f"\nGenerating segment: {segment_name}...")
            start_time = time.time()
            
            segment_content = self.generate_segment(
                segment_name,
                info["words"],
                pdf_content,
                conversation_history,
                pdf_path
            )
            
            end_time = time.time()
            print(f"Segment '{segment_name}' generated in {end_time - start_time:.2f} seconds")
            
            # Update conversation history and script
            conversation_history += "\n" + self.extract_last_words(segment_content)
            complete_script += f"\n\n{segment_content}\n"
            
            # Add a delay to avoid hitting rate limits
            time.sleep(3)
        
        # Determine first speaker by checking who introduces themselves first
        first_speaker = "Vic" if "I'm Vic" in complete_script else "Alex"
        pdf_name = self.clean_filename(os.path.basename(pdf_path))
        output_path = f"scripts/{pdf_name}_{first_speaker}_first.txt"
        
        # Save the complete script
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(complete_script)
        
        return complete_script, output_path

def main():
    """Main function to generate a podcast script from a PDF file."""
    generator = ScriptGenerator()
    
    # Find the only PDF file in the pdfs directory
    pdf_dir = "pdfs"
    if not os.path.exists(pdf_dir):
        print(f"Error: Directory '{pdf_dir}' not found.")
        return
    
    pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"Error: No PDF files found in '{pdf_dir}' directory.")
        return
    
    if len(pdf_files) > 1:
        print(f"Error: Multiple PDF files found in '{pdf_dir}' directory. Please ensure only one PDF file is present.")
        return
    
    pdf_path = os.path.join(pdf_dir, pdf_files[0])
    print(f"Using PDF file: {pdf_path}")
    
    try:
        script, output_path = generator.generate_full_script(pdf_path)
        print(f"\nScript generated successfully! Saved to: {output_path}")
        print("\nPreview of the generated script:")
        print(script[:500] + "...")  # Show first 500 characters
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
