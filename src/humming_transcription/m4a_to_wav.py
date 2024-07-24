from pydub import AudioSegment

def convert_m4a_to_wav(input_file, output_file):
    # m4aファイルを読み込む
    audio = AudioSegment.from_file(input_file, format="m4a")
    
    # wavファイルに変換して保存する
    audio.export(output_file, format="wav")
    print(f"Converted {input_file} to {output_file}")

# 使用例
input_file = "./record/sad/input.m4a"
output_file = "./record/sad/output.wav"
convert_m4a_to_wav(input_file, output_file)
