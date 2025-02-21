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
        # Define the structure we want the LLM to follow
        function_schema = {
            "name": "format_text",
            "description": "Format and clean text for text-to-speech conversion",
            "parameters": {
                "type": "object",
                "properties": {
                    "formatted_text": {
                        "type": "string",
                        "description": "The cleaned and formatted text"
                    },
                    "statistics": {
                        "type": "object",
                        "properties": {
                            "original_length": {"type": "integer"},
                            "formatted_length": {"type": "integer"},
                            "removed_duplicates": {"type": "integer"}
                        }
                    }
                },
                "required": ["formatted_text", "statistics"]
            }
        }

        # Create the system message with formatting instructions
        system_message = """You are a text formatting assistant that prepares text for text-to-speech conversion.
        Your tasks:
        1. Remove any duplicate sentences or paragraphs
        2. Fix formatting issues from PDF extraction
        3. Ensure proper spacing and punctuation
        4. Remove unnecessary whitespace and special characters
        5. Maintain the logical flow of the content
        6. Keep important information while removing redundancy
        7. Format numbers and symbols for better speech output
        8. Structure the text in a way that sounds natural when spoken
        
        Return the formatted text and statistics about the changes made."""

        # Create the completion request
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": f"Format this text for text-to-speech: {text}"}
            ],
            functions=[function_schema],
            function_call={"name": "format_text"}
        )

        # Parse the response
        result = json.loads(response.choices[0].message.function_call.arguments)
        
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