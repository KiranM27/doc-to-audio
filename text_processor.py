"""Module for text processing operations"""
import math

def split_text(text, max_length=4000):
    """Split text into chunks of maximum length while preserving sentence boundaries."""
    if len(text) <= max_length:
        return [text]
    
    chunks = []
    sentences = text.split('. ')
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 2 <= max_length:
            current_chunk += sentence + '. '
        else:
            chunks.append(current_chunk)
            current_chunk = sentence + '. '
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks

def calculate_costs(text):
    """Calculate costs for both text formatting and TTS."""
    char_count = len(text)
    
    # GPT-3.5 Turbo costs (as of 2024)
    # $0.0010 per 1K tokens (input)
    # Approximate tokens as characters/4 for English text
    estimated_tokens = math.ceil(char_count / 4)
    gpt_cost = (estimated_tokens / 1000) * 0.0010
    
    # TTS costs
    # OpenAI charges $0.015 per 1,000 characters
    tts_cost = (char_count / 1000) * 0.015
    
    return {
        'characters': char_count,
        'chunks': math.ceil(char_count / 4000),
        'tokens': estimated_tokens,
        'gpt_cost': round(gpt_cost, 3),
        'tts_cost': round(tts_cost, 2),
        'total_cost': round(gpt_cost + tts_cost, 2)
    } 