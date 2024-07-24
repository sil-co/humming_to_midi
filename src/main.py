from hamming_transcription.record_audio import record_audio
from hamming_transcription.wav_to_midi import wav_to_midi
from hamming_transcription.midi_to_audio import midi_to_audio

def main():
    audio_file = 'humming.wav'
    midi_file = 'output.mid'
    output_audio = 'output.wav'
    
    # # Record audio
    # record_audio(audio_file)
    
    # Convert audio to MIDI
    wav_to_midi(audio_file, midi_file)
    
    # Convert MIDI to audio
    midi_to_audio(midi_file, output_audio)
    
    print(f"Conversion complete. Check the output file: {output_audio}")

if __name__ == "__main__":
    main()
