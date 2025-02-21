"""Main module for PDF to Speech conversion"""
import os
from processor import DocumentProcessor

def get_user_confirmation(prompt):
    """Get user confirmation to proceed."""
    proceed = input(f"\n  {prompt} (y/n): ")
    return proceed.lower() == "y"

def main():
    """Entry point of the application."""
    try:
        processor = DocumentProcessor()
        pdf_path = os.path.join("inputs", "DeFiTradingResearch.pdf")

        test_mode = get_user_confirmation("Would you like to run in test mode (process only first chunk)?")
        raw_text, output_path = processor.process_document(pdf_path, test_mode)

        use_formatting = get_user_confirmation("Would you like to use AI text formatting to improve speech quality?")
        processor.estimate_costs(raw_text, use_formatting)

        if not get_user_confirmation("Do you want to proceed with the conversion?"):
            print("🛑 Operation cancelled.")
            return
        
        processor.convert_to_audio(raw_text, output_path, use_formatting, test_mode)
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
