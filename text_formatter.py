"""Module for formatting text using OpenAI's Chat Completion API"""
import json
import openai

def format_text_for_tts(text: str) -> str:
    """
    Format text for text-to-speech using OpenAI's Chat Completion API.
    Removes duplicates, fixes formatting issues, and structures the text for better TTS output.
    """
    print("\n🔄 Formatting text for better speech output...")
    
    try:
        # Create the system message with formatting instructions
        system_message = """You are a text formatting assistant that prepares text for text-to-speech conversion.
        Your task is to format the input text and return a JSON object with the following:
        1. A 'formatted_text' field containing the processed text with:
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
        
        Ensure your response is a valid JSON object with these fields."""

        # Create the completion request
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": "Please format the following text and return a JSON response with the formatting results: " + text}
            ]
        )

        # Parse the response
        result = json.loads(response.choices[0].message.content)
        
        # Display statistics
        stats = result['statistics']
        print("\n📊 Formatting Statistics:")
        print(f"📝 Original length: {stats['original_length']} characters")
        print(f"✨ Formatted length: {stats['formatted_length']} characters")
        print(f"🔄 Removed duplicates: {stats['removed_duplicates']}")
        
        return result['formatted_text']

    except Exception as e:
        print(f"❌ Error formatting text: {str(e)}")
        return text  # Return original text if formatting fails 