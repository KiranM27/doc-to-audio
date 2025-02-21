"""Module for audio processing operations"""
import os
from pydub import AudioSegment
from tqdm import tqdm
import openai
from datetime import datetime

def create_audio_chunk(chunk, output_file, voice="alloy"):
    """Creates a single audio chunk from text."""
    with open(output_file, 'wb') as f:
        response = openai.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=chunk
        )
        f.write(response.read())

def combine_audio_files(base_filename, num_chunks):
    """Combines multiple MP3 files into a single audio file."""
    print("\n🎵 Combining audio chunks...")
    base_name, ext = os.path.splitext(base_filename)
    
    combined = AudioSegment.from_mp3(f"{base_name}_part1{ext}")
    
    for i in tqdm(range(2, num_chunks + 1), desc="Combining chunks", unit="chunk"):
        chunk_path = f"{base_name}_part{i}{ext}"
        audio_chunk = AudioSegment.from_mp3(chunk_path)
        combined += audio_chunk
        os.remove(chunk_path)
    
    print(f"🗑️  Cleaned up temporary chunk files")
    combined.export(base_filename, format="mp3")
    print(f"✨ Combined audio saved to {base_filename}")

def process_text_to_speech(text, output_file="output.mp3", voice="alloy"):
    """Processes text to speech conversion with timing and progress tracking."""
    try:
        from text_processor import split_text
        chunks = split_text(text)
        start_time = datetime.now()
        
        # Ensure temporary files go to outputs directory
        base_name, ext = os.path.splitext(output_file)
        temp_base = os.path.join('outputs', os.path.basename(base_name))
        
        if len(chunks) > 1:
            print(f"\n🎤 Converting text to speech in {len(chunks)} chunks...")
            
            for i, chunk in enumerate(tqdm(chunks, desc="Processing chunks", unit="chunk"), 1):
                chunk_file = f"{temp_base}_part{i}{ext}"
                create_audio_chunk(chunk, chunk_file, voice)
            
            combine_audio_files(output_file, len(chunks))
        else:
            print("\n🎤 Converting text to speech...")
            create_audio_chunk(chunks[0], output_file, voice)
            print(f"✨ Audio saved to {output_file}")
        
        duration = datetime.now() - start_time
        print(f"⏱️  Total processing time: {duration.total_seconds():.1f} seconds")
            
    except Exception as e:
        print(f"❌ Error generating speech: {str(e)}") 