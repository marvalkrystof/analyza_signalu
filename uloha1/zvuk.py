import numpy as np
import soundfile as sf
from scipy import signal
import sounddevice as sd

# definování funkce pro normalizaci audio signálu
def normalize(audio):
    peak = np.max(np.abs(audio))
    return audio / peak if peak > 0 else audio.copy()


# Načteme audio soubor a jeho vzorkovací frekvenci
audio, sample_rate = sf.read("breath.mp3")

print(f"Audio data shape: {audio.shape}")
print(f"Sample rate: {sample_rate}")

# decimace a snížení vzorkovací frekvence o faktor 16
audio_decimated = signal.decimate(audio, 16, axis=0)
sample_rate_decimated = sample_rate // 16

audio_decimated = normalize(audio_decimated)

# spustíme originální audio
# sd.play(audio, sample_rate)
# sd.wait()

# spustíme audio
sd.play(audio_decimated, sample_rate_decimated)
sd.wait()

# vybereme každý 16. vzorek z původního audio signálu
audio_subsampled = audio[::16]
audio_subsampled = normalize(audio_subsampled)

# spustíme subsampled audio
sd.play(audio_subsampled, sample_rate_decimated)
sd.wait()

# subsampling pouze bere každý 16. vzorek, ale nedělá filtraci.
# Decimace nejdříve aplikuje low-pass filtr, aby odstranila vysokofrekvenční složky, a poté provede subsampling. 
# To je důležité, protože bez filtrace by mohlo dojít k aliasingu, což by mohlo způsobit zkreslení zvuku tím, že vytvoří "falešné" frekvence, které se ve zvuku původně nevyskytovaly, z vysokofrekvenčních složek původního signálu.