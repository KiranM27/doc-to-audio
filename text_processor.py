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

def calculate_tts_cost(text):
    """Calculate character count and estimated cost for TTS."""
    char_count = len(text)
    # OpenAI charges $0.015 per 1,000 characters
    estimated_cost = (char_count / 1000) * 0.06
    
    return {
        'characters': char_count,
        'chunks': math.ceil(char_count / 4000),
        'estimated_cost': round(estimated_cost, 2)
    } 