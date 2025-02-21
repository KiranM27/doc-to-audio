"""Module for formatting text using OpenAI's Chat Completion API"""
import json
import openai
from helpers import retry_on_error

@retry_on_error(max_attempts=3, delay_seconds=2)
def format_text_for_tts(text: str) -> str:
    """
    Format text for text-to-speech using OpenAI's Chat Completion API.
    Retries up to 3 times on failure with 2-second delay between attempts.
    """
    # Create the system message with formatting instructions
    system_message = """You are a text formatting assistant that prepares text for text-to-speech conversion.
    Your task is to format the input text and return a JSON object with the following:
    1. A 'formatted_text' field containing the processed text with:
       - Only make changes to the text if it is necessary to improve the text-to-speech output. Else keep the text as it. 
       - Do not remove text unless it is necessary to improve the text-to-speech output.
       - Removed duplicate sentences or paragraphs
       - Fixed formatting issues from PDF extraction
       - Proper spacing and punctuation
       - No unnecessary whitespace or special characters
       - Maintained logical flow
       - Important information preserved while removing redundancy
       - Numbers and symbols formatted for better speech output
       - Natural speech-friendly structure
    
    2. A 'statistics' object containing:
       - original_length: number of characters in input
       - formatted_length: number of characters in output
       - removed_duplicates: number of duplicates removed
    
    Important: Your response must be a valid JSON object with these exact fields."""

    try:
        # Create the completion request
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": "Format the following text and return a JSON response: " + text}
            ]
        )

        # Parse and validate the response
        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty response from OpenAI")

        result = json.loads(content)
        
        # Validate required fields
        if 'formatted_text' not in result:
            raise ValueError("Missing 'formatted_text' in response")
        if 'statistics' not in result:
            raise ValueError("Missing 'statistics' in response")
            
        return result['formatted_text']

    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {str(e)}")
        print("Response content:", content)
        raise ValueError(f"Invalid JSON response from OpenAI: {str(e)}")
    except Exception as e:
        print(f"❌ Formatting error: {str(e)}")
        raise

