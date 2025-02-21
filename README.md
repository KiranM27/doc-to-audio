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

## Key Benefits

- Automatically removes duplicate content from PDF extraction
- Fixes formatting issues and improves text structure
- Optimizes text for natural-sounding speech output
- Maintains logical flow while removing redundancy
- Properly formats numbers and symbols for speech

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
   - Display text statistics and estimated cost
   - Ask for confirmation before proceeding
   - Convert the text to speech
   - Save the audio file in the `outputs` directory

## Project Structure

```
doc-to-audio/
├── inputs/             # Directory for input PDF files
├── outputs/            # Directory for output audio files
├── main.py            # Main script
├── audio_processor.py # Audio processing functions
├── pdf_processor.py   # PDF handling functions
├── text_processor.py  # Text processing functions
└── .env              # Environment variables
```

## Cost Estimation

The script provides an estimate of the conversion cost based on OpenAI's pricing:
- $0.015 per 1,000 characters
- Automatic text chunking (4000 characters per chunk)
- Cost estimate displayed before conversion

## Error Handling

The script includes comprehensive error handling for:
- Missing API keys
- PDF reading errors
- Text processing issues
- Audio conversion problems

## Contributing

Feel free to open issues or submit pull requests for any improvements.

## License

[MIT License](LICENSE) 