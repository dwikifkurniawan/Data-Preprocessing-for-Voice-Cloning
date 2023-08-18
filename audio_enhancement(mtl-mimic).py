import torchaudio
from speechbrain.pretrained import WaveformEnhancement

enhance_model = WaveformEnhancement.from_hparams(
    source="speechbrain/mtl-mimic-voicebank",
    savedir="pretrained_models/mtl-mimic-voicebank",
)
print("Enhancing audio...")
enhanced = enhance_model.enhance_file("test.wav")

# Saving enhanced signal on disk
output_name = "test(mtl-mimic).wav"
torchaudio.save(f'{output_name}', enhanced.unsqueeze(0).cpu(), 16000)
print("Done!")