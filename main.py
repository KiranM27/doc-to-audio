"""Main module for PDF to Speech conversion"""

import os
from dotenv import load_dotenv
import openai
from pdf_processor import extract_text_from_pdf
from text_processor import calculate_tts_cost
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


def display_statistics(stats):
    """Display text statistics and cost information."""
    print("\n📊 Text Statistics:")
    print(f"📝 Characters: {stats['characters']:,}")
    print(f"📦 Number of chunks needed: {stats['chunks']}")
    print(f"💰 Estimated cost: ${stats['estimated_cost']}")


def get_user_confirmation():
    """Get user confirmation to proceed."""
    proceed = input(
        "\n⚠️  Do you want to proceed with text-to-speech conversion? (y/n): "
    )
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

        text = extract_text_from_pdf(pdf_path)

        if not text.strip():
            print("❌ No text could be extracted from the PDF.")
            return

        stats = calculate_tts_cost(text)
        display_statistics(stats)

        if not get_user_confirmation():
            print("🛑 Operation cancelled.")
            return

        process_text_to_speech(text, output_file=output_path, voice="alloy")
        print("\n✅ All done!")

    except Exception as e:
        print(f"❌ Error: {str(e)}")


def main():
    """Entry point of the application."""
    pdf_path = os.path.join("inputs", "DeFiTradingResearch.pdf")
    runner(pdf_path)


if __name__ == "__main__":
    main()
