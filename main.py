"""Main module for PDF to Speech conversion"""

import os
from dotenv import load_dotenv
import openai
from pdf_processor import extract_text_from_pdf
from text_processor import calculate_costs, split_text
from text_formatter import format_text_for_tts
from audio_processor import process_text_to_speech

# Create necessary directories
def ensure_directories():
    """Ensure inputs and outputs directories exist."""
    os.makedirs("inputs", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

def initialize_openai():
    """Initialize OpenAI with API key from environment."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("❌ OPENAI_API_KEY not found in environment variables")
    openai.api_key = api_key


def display_statistics(stats, show_formatting_cost=True):
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


def get_user_confirmation(prompt):
    """Get user confirmation to proceed."""
    proceed = input(f"\n⚠️  {prompt} (y/n): ")
    return proceed.lower() == "y"


def runner(pdf_path):
    """Main function to process a PDF file to speech."""
    print("\n🚀 Starting PDF to Speech Converter")

    try:
        ensure_directories()
        initialize_openai()

        # Get the PDF filename and create output path
        pdf_filename = os.path.basename(pdf_path)
        output_filename = os.path.splitext(pdf_filename)[0] + '.mp3'
        output_path = os.path.join('outputs', output_filename)

        # Extract text from PDF
        raw_text = extract_text_from_pdf(pdf_path)

        if not raw_text.strip():
            print("❌ No text could be extracted from the PDF.")
            return

        # Calculate initial TTS costs (without formatting)
        initial_stats = calculate_costs(raw_text)
        print("\n💡 Cost estimate for basic conversion (without text formatting):")
        display_statistics(initial_stats, show_formatting_cost=False)

        # Ask if user wants to use text formatting
        use_formatting = get_user_confirmation("Would you like to use AI text formatting to improve speech quality?")
        
        if use_formatting:
            print("\n💡 Cost estimate with text formatting:")
            display_statistics(initial_stats, show_formatting_cost=True)
        
        # Ask for final confirmation
        if not get_user_confirmation("Do you want to proceed with the conversion?"):
            print("🛑 Operation cancelled.")
            return

        final_text = raw_text
        if use_formatting:
            print("\n🔄 Formatting text chunks for better speech output...")
            # Split text into chunks for formatting (max 4000 tokens per request)
            text_chunks = split_text(raw_text, max_length=16000)  # 4000 tokens ≈ 16000 chars
            formatted_chunks = []
            
            for i, chunk in enumerate(text_chunks, 1):
                print(f"\n📝 Formatting chunk {i} of {len(text_chunks)}...")
                formatted_chunk = format_text_for_tts(chunk)
                formatted_chunks.append(formatted_chunk)
            
            final_text = " ".join(formatted_chunks)
            print("\n✨ Text formatting complete!")

        process_text_to_speech(final_text, output_file=output_path, voice="alloy")
        print("\n✅ All done!")

    except Exception as e:
        print(f"❌ Error: {str(e)}")


def main():
    """Entry point of the application."""
    pdf_path = os.path.join("inputs", "DeFiTradingResearch.pdf")
    runner(pdf_path)


if __name__ == "__main__":
    main()
