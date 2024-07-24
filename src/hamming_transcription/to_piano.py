import librosa
import numpy as np
from midiutil import MIDIFile
import pretty_midi
from scipy.io import wavfile

# 1. 音声ファイルを読み込む
y, sr = librosa.load("humming.wav")  # または 'humming.m4a'

# 2. ピッチ検出を行う
pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

# 3. 各フレームの最も強いピッチを取得
pitch_values = []
for t in range(len(pitches[0])):
    index = magnitudes[:, t].argmax()
    pitch_values.append(pitches[index, t])

# 4. MIDI ノートに変換
midi_notes = librosa.hz_to_midi(pitch_values)

# 5. MIDI ファイルを生成
midi = MIDIFile(1)
track = 0
time = 0
midi.addTrackName(track, time, "Humming to Piano")
midi.addTempo(track, time, 120)

for note in midi_notes:
    if note > 0:  # 無音でない場合
        midi.addNote(track, 0, int(round(note)), time, 0.5, 100)
    time += 0.5

# MIDI ファイルを保存
with open("piano_output.mid", "wb") as output_file:
    midi.writeFile(output_file)

# 6. MIDI を WAV に変換
# MIDIファイルを読み込む
midi_data = pretty_midi.PrettyMIDI("piano_output.mid")

# オーディオデータを生成
audio_data = midi_data.synthesize(fs=44100)

# WAVファイルとして保存
wavfile.write("piano_output.wav", 44100, (audio_data * 32767).astype(np.int16))

print("変換が完了しました。'piano_output.wav'が生成されました。")
