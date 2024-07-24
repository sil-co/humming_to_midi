import librosa
import numpy as np
from midiutil import MIDIFile
import pretty_midi
from scipy.io import wavfile
import soundfile as sf

# ノイズリダクション関数
def reduce_noise(y, sr):
    # スペクトログラムを計算
    S = librosa.stft(y)
    # ノイズプロファイルを推定（最初の0.5秒を使用）
    noise_profile = np.mean(np.abs(S[:, :int(0.5 * sr / librosa.hop_length)]), axis=1)
    # スペクトル減算
    S_reduced = S - noise_profile[:, np.newaxis]
    S_reduced = np.maximum(S_reduced, 0)  # 負の値を0に設定
    # 逆STFTを適用して時間領域信号に戻す
    y_reduced = librosa.istft(S_reduced)
    return y_reduced

# 1. 音声ファイルを読み込む
y, sr = librosa.load('humming.wav', duration=10)  # 10秒に制限

# 2. ノイズリダクションを適用
y_reduced = reduce_noise(y, sr)

# 3. ピッチ検出を行う
pitches, magnitudes = librosa.piptrack(y=y_reduced, sr=sr)

# 4. 各フレームの最も強いピッチを取得（閾値を設定）
pitch_values = []
magnitude_threshold = np.max(magnitudes) * 0.1  # 最大マグニチュードの10%を閾値とする
for t in range(len(pitches[0])):
    index = magnitudes[:, t].argmax()
    if magnitudes[index, t] > magnitude_threshold:
        pitch_values.append(pitches[index, t])
    else:
        pitch_values.append(0)  # 閾値以下のマグニチュードは無音とする

# 5. MIDI ノートに変換
midi_notes = librosa.hz_to_midi(np.array(pitch_values))
midi_notes = [note for note in midi_notes if note > 0]  # 0（無音）を除去

# 6. MIDI ファイルを生成
midi = MIDIFile(1)
track = 0
time = 0
midi.addTrackName(track, time, "Humming to Piano")
midi.addTempo(track, time, 120)

for note in midi_notes:
    midi.addNote(track, 0, int(round(note)), time, 0.25, 100)  # ノートの長さを0.25秒に設定
    time += 0.25

# MIDI ファイルを保存
with open("piano_output.mid", "wb") as output_file:
    midi.writeFile(output_file)

# 7. MIDI を WAV に変換
midi_data = pretty_midi.PrettyMIDI('piano_output.mid')
audio_data = midi_data.synthesize(fs=44100)
wavfile.write('piano_output.wav', 44100, (audio_data * 32767).astype(np.int16))

# 8. ノイズリダクション後の音声を保存（オプション）
sf.write('humming_reduced_noise.wav', y_reduced, sr)

print("変換が完了しました。'piano_output.wav'が生成されました。")
print("ノイズリダクション後の音声が'humming_reduced_noise.wav'として保存されました。")