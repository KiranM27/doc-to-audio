"""Main module for PDF to Speech conversion"""

import os
from dotenv import load_dotenv
import openai
from datetime import datetime
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


def get_timestamped_filename(base_name: str, test_mode: bool) -> str:
    """Generate a filename with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix = '_test' if test_mode else ''
    return f"{base_name}{suffix}_{timestamp}.mp3"


def runner(pdf_path, test_mode=True):
    """Main function to process a PDF file to speech."""
    print("\n🚀 Starting PDF to Speech Converter")
    if test_mode:
        print("🧪 Running in test mode - will only process first chunk")

    try:
        ensure_directories()
        initialize_openai()

        # Get the PDF filename and create output path with timestamp
        pdf_filename = os.path.basename(pdf_path)
        base_name = os.path.splitext(pdf_filename)[0]
        output_filename = get_timestamped_filename(base_name, test_mode)
        output_path = os.path.join('outputs', output_filename)
        
        print(f"📝 Output will be saved as: {output_filename}")

        # Extract text from PDF
        raw_text = extract_text_from_pdf(pdf_path)

        if not raw_text.strip():
            print("❌ No text could be extracted from the PDF.")
            return

        # In test mode, only take the first chunk
        if test_mode:
            chunks = split_text(raw_text, max_length=1600)  # 400 tokens ≈ 1600 chars
            raw_text = chunks[0]
            print(f"\n📝 Test mode: Using first chunk ({len(raw_text)} characters)")

        # Ask if user wants to use text formatting
        use_formatting = get_user_confirmation("Would you like to use AI text formatting to improve speech quality?")
        
        # Calculate and display costs based on user's choice
        initial_stats = calculate_costs(raw_text)
        print("\n💡 Cost estimate for conversion:")
        display_statistics(initial_stats, show_formatting_cost=use_formatting)
        
        # Ask for final confirmation
        if not get_user_confirmation("Do you want to proceed with the conversion?"):
            print("🛑 Operation cancelled.")
            return

        final_text = raw_text
        if use_formatting:
            print("\n🔄 Formatting text for better speech output...")
            final_text = format_text_for_tts(raw_text)
            print("\n✨ Text formatting complete!")

        process_text_to_speech(final_text, output_file=output_path, voice="alloy")
        print("\n✅ All done!")
        
        if test_mode:
            print("\n🧪 Test completed successfully! Check the output file for quality.")
            print("If you're satisfied with the result, run the script without test mode for the full document.")

    except Exception as e:
        print(f"❌ Error: {str(e)}")


def main():
    """Entry point of the application."""
    pdf_path = os.path.join("inputs", "DeFiTradingResearch.pdf")
    
    # Ask if user wants to run in test mode
    test_mode = get_user_confirmation("Would you like to run in test mode (process only first chunk)?")
    runner(pdf_path, test_mode=test_mode)


if __name__ == "__main__":
    main()
