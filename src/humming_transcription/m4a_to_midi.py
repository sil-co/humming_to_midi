import librosa
import pretty_midi
import numpy as np
from pydub import AudioSegment

def audio_to_midi(input_file, output_midi):
    # M4AファイルをWAVに変換
    audio = AudioSegment.from_file(input_file, format="m4a")
    audio.export("temp.wav", format="wav")
    
    # 以降は元のコードと同じ
    y, sr = librosa.load("temp.wav")
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    
    midi = pretty_midi.PrettyMIDI()
    piano_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')
    piano = pretty_midi.Instrument(program=piano_program)
    
    time_step = librosa.frames_to_time(np.arange(len(pitches)), sr=sr)
    notes = []
    
    for t in range(len(pitches[0])):
        pitch = pitches[:, t]
        pitch = pitch[pitch > 0]
        
        if len(pitch) > 0:
            note_number = int(np.mean(librosa.hz_to_midi(pitch)))
            note = pretty_midi.Note(velocity=100, pitch=note_number, start=time_step[t], end=time_step[t] + 0.1)
            notes.append(note)
    
    piano.notes = notes
    midi.instruments.append(piano)
    
    midi.write(output_midi)

if __name__ == "__main__":
    audio_to_midi('humming.m4a', 'output.mid')