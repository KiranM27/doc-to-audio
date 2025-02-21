"""Core processing module for PDF to Audio conversion"""
import os
from datetime import datetime
from tqdm import tqdm
import openai
from dotenv import load_dotenv

from pdf_processor import extract_text_from_pdf
from text_processor import calculate_costs, split_text
from text_formatter import format_text_for_tts
from audio_processor import process_text_to_speech

class DocumentProcessor:
    def __init__(self):
        self.ensure_directories()
        self.initialize_openai()

    def ensure_directories(self):
        """Ensure inputs and outputs directories exist."""
        os.makedirs("inputs", exist_ok=True)
        os.makedirs("outputs", exist_ok=True)

    def initialize_openai(self):
        """Initialize OpenAI with API key from environment."""
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("❌ OPENAI_API_KEY not found in environment variables")
        openai.api_key = api_key

    def get_timestamped_filename(self, base_name: str, test_mode: bool) -> str:
        """Generate a filename with timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        suffix = '_test' if test_mode else ''
        return f"{base_name}{suffix}_{timestamp}.mp3"

    def display_statistics(self, stats, show_formatting_cost=True):
        """Display text statistics and cost information."""
        print("\n📊 Text Statistics:")
        print(f"📝 Characters: {stats['characters']:,}")
        print(f"🔤 Estimated tokens: {stats['tokens']:,}")
        print(f"📦 Number of chunks needed: {stats['chunks']}")
        print("\n💰 Cost Breakdown:")
        if show_formatting_cost:
            print(f"🧠 Text formatting (GPT): ${stats['gpt_cost']}")
        print(f"🔊 Text-to-Speech: ${stats['tts_cost']}")
        print(f"📈 Total estimated cost: ${stats['total_cost'] if show_formatting_cost else stats['tts_cost']}")

    def format_text_chunks(self, text: str) -> str:
        """Format text in chunks using GPT."""
        print("\n🔄 Formatting text chunks for better speech output...")
        # Split into smaller chunks for GPT (max ~16K tokens ≈ 64K chars)
        # Using 12K tokens (48K chars) to be safe
        format_chunks = split_text(text, max_length=48000)
        formatted_chunks = []
        
        for i, chunk in enumerate(tqdm(format_chunks, desc="Formatting chunks", unit="chunk")):
            print(f"\n📝 Processing chunk {i+1} of {len(format_chunks)}")
            formatted_chunk = format_text_for_tts(chunk)
            formatted_chunks.append(formatted_chunk)
        
        final_text = " ".join(formatted_chunks)
        print(f"\n✨ Text formatting complete! Processed {len(format_chunks)} chunks")
        return final_text

    def process_document(self, pdf_path: str, test_mode: bool = True) -> str:
        """Process a PDF document and convert it to audio."""
        print("\n🚀 Starting PDF to Speech Converter")
        if test_mode:
            print("🧪 Running in test mode - will only process first chunk")

        # Get the PDF filename and create output path with timestamp
        pdf_filename = os.path.basename(pdf_path)
        base_name = os.path.splitext(pdf_filename)[0]
        output_filename = self.get_timestamped_filename(base_name, test_mode)
        output_path = os.path.join('outputs', output_filename)
        
        print(f"📝 Output will be saved as: {output_filename}")

        # Extract and process text
        raw_text = extract_text_from_pdf(pdf_path)
        if not raw_text.strip():
            raise ValueError("❌ No text could be extracted from the PDF.")

        # In test mode, only take the first chunk
        if test_mode:
            chunks = split_text(raw_text, max_length=1600)  # 400 tokens ≈ 1600 chars
            raw_text = chunks[0]
            print(f"\n📝 Test mode: Using first chunk ({len(raw_text)} characters)")

        return raw_text, output_path

    def estimate_costs(self, text: str, use_formatting: bool) -> dict:
        """Calculate and display cost estimates."""
        stats = calculate_costs(text)
        print("\n💡 Cost estimate for conversion:")
        self.display_statistics(stats, show_formatting_cost=use_formatting)
        return stats

    def convert_to_audio(self, text: str, output_path: str, use_formatting: bool, test_mode: bool) -> None:
        """Convert text to audio with optional formatting."""
        final_text = self.format_text_chunks(text) if use_formatting else text
        
        process_text_to_speech(final_text, output_file=output_path, voice="alloy")
        print("\n✅ All done!")
        
        if test_mode:
            print("\n🧪 Test completed successfully! Check the output file for quality.")
            print("If you're satisfied with the result, run the script without test mode for the full document.") 