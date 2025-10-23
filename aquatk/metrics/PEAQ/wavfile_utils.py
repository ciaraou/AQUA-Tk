import numpy as np
import struct
import soundfile as sf
from scipy.io import wavfile
import math
import wave


def read_wav_blocks(filename, block_size=2048, overlap=1024):
    blocks = []
    with wave.open(filename, "rb") as wav_file:
        n_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        frame_rate = wav_file.getframerate()
        n_frames = wav_file.getnframes()
        n_blocks = 1 + (n_frames - block_size) // (block_size - overlap)
        # Determine the data type based on the sample width
        if sample_width == 1:
            dtype = "u1"  # 8-bit PCM
        elif sample_width == 2:
            dtype = "i2"  # 16-bit PCM
        elif sample_width == 3:
            dtype = "i3"  # 24-bit PCM
        elif sample_width == 4:
            dtype = "i4"  # 32-bit PCM
        else:
            raise ValueError(f"Unsupported sample width: {sample_width}")

        step_size = block_size - overlap
        # Read blocks
        for i in range(n_blocks):
            wav_file.setpos(i * step_size)
            # Read block_size frames
            frames = wav_file.readframes(block_size)
            if len(frames) < block_size * sample_width:
                # If we've reached the end of the file, we can break out of the loop.
                break

            # Convert byte data to numpy array

            block = np.frombuffer(frames, dtype=dtype)

            block = block.reshape(-1, n_channels)

            blocks.append(block)

            # Rewind for overlap
    print(f"Expected blocks from wav: {1 + (n_frames - block_size) // step_size}")
    print(np.array(blocks).dtype)
    print(np.array(blocks).max(), np.array(blocks).min())
    return blocks

def librosa_to_wav_blocks(audio, sr, block_size=2048, overlap=1024, bit_depth=16):
    blocks = []
    
    if audio.ndim == 1:
        n_channels = 1
        n_frames = len(audio)
        audio_2d = audio.reshape(-1, 1)
    else:
        n_channels = audio.shape[0]
        n_frames = audio.shape[1]
        audio_2d = audio.T 
    
    # Convert float to integer PCM
    if bit_depth == 16:
        dtype = np.int16
        max_val = 32768
    elif bit_depth == 24:
        dtype = np.int32
        max_val = 8388608
    elif bit_depth == 32:
        dtype = np.int32
        max_val = 2147483648
    else:
        raise ValueError(f"Unsupported bit depth: {bit_depth}")
    
    audio_int = np.clip(audio_2d * max_val, -max_val, max_val - 1).astype(dtype)
    
    # blocks based on read_wav_blocks
    step_size = block_size - overlap
    n_blocks = 1 + (n_frames - block_size) // step_size
    
    for i in range(n_blocks):
        start = i * step_size
        end = start + block_size
        
        if end > n_frames:
            break
        
        block = audio_int[start:end]  # (block_size, n_channels)
        blocks.append(block)
    
    if len(blocks) > 0:
        print(f"Created {len(blocks)} blocks")
        print(blocks[0].dtype)
        print(np.max([b.max() for b in blocks]), np.min([b.min() for b in blocks]))
    
    return blocks