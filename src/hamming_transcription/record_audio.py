import pyaudio
import wave

def record_audio(output_file, record_seconds=10, sample_rate=44100, chunk=1024, channels=1):
    audio = pyaudio.PyAudio()
    
    stream = audio.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk)
    
    print("Recording...")
    frames = []
    
    for _ in range(0, int(sample_rate / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)
    
    print("Finished recording.")
    
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))
        
if __name__ == "__main__":
    record_audio('humming.wav')
