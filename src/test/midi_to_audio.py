from midi2audio import FluidSynth

def midi_to_audio(input_midi, output_audio):
    fs = FluidSynth()
    fs.midi_to_audio(input_midi, output_audio)

if __name__ == "__main__":
    midi_to_audio('output.mid', 'output.wav')

