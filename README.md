# Document to Audio Converter

Convert your PDF documents into high-quality audio files using OpenAI's Text-to-Speech API.

## Features

- PDF text extraction with PyPDF2
- Smart text formatting using OpenAI's GPT model
- High-quality text-to-speech conversion using OpenAI's TTS API
- Efficient processing of large documents through chunking
- Cost estimation before conversion
- Progress tracking with detailed status updates
- Multiple voice options (default: alloy)
- Test mode for quality verification
- Automatic retry mechanism for error recovery

## Key Benefits

- Intelligent text preprocessing for better speech output
- Preserves important information while fixing formatting issues
- Handles large documents efficiently through smart chunking
- Provides detailed cost estimates before processing
- Test mode to verify quality before full conversion
- Timestamps in output files for version tracking

## Prerequisites

- Python 3.7+
- OpenAI API key
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/KiranM27/doc-to-audio.git
cd doc-to-audio
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your OpenAI API key:
```bash
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Place your PDF file in the `inputs` directory.

2. Run the converter:
```bash
python main.py
```

3. The script will:
   - Ask if you want to run in test mode (processes only first chunk)
   - Display text statistics and estimated cost
   - Ask if you want to use text formatting
   - Show final cost estimate based on your choices
   - Ask for confirmation before proceeding
   - Convert the text to speech
   - Save the audio file with timestamp in the `outputs` directory

## Project Structure

```
doc-to-audio/
├── inputs/             # Directory for input PDF files
├── outputs/           # Directory for output audio files
├── main.py           # Main script and user interaction
├── processor.py      # Core processing logic
├── audio_processor.py # Audio processing functions
├── pdf_processor.py  # PDF handling functions
├── text_processor.py # Text processing functions
├── text_formatter.py # Text formatting with GPT
├── helpers.py        # Utility functions and decorators
└── .env             # Environment variables
```

## Text Processing Features

- Removes duplicate content only when necessary
- Fixes PDF extraction formatting issues
- Ensures proper spacing and punctuation
- Maintains logical flow of content
- Formats numbers and symbols for better speech
- Processes text in small chunks for reliability
- Automatic retry on formatting errors

## Error Handling

The script includes comprehensive error handling for:
- Missing API keys
- PDF reading errors
- Text processing issues
- JSON parsing errors
- Network connectivity issues
- Rate limiting
- Audio conversion problems

## Output Files

Output files are automatically named with:
- Original PDF name
- Test mode indicator (if applicable)
- Timestamp for version tracking
Example: `document_test_20240220_143022.mp3`

## Contributing

Feel free to open issues or submit pull requests for any improvements.

## License

[MIT License](LICENSE) 