"""Vygeneruje sedm signalu a jejich jednostranna amplitudova spektra do PDF."""

import os
from pathlib import Path
import tempfile

import numpy as np

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "uloha2-matplotlib"))
import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


N = 512
VYSTUP = Path(__file__).resolve().parent / "output" / "pdf" / "spektra_signalu.pdf"


def signaly():
    """Vrati (popis, vzorkovaci frekvence, vzorky, jednotka, typ grafu)."""
    fs = 256
    t = np.arange(N) / fs
    yield "a) Sinus 10 Hz, amplituda 10 mV", fs, 10 * np.sin(2 * np.pi * 10 * t), "mV", "line"
    trojuhelnik = 10 * (2 / np.pi) * np.arcsin(np.sin(2 * np.pi * 10 * t))
    yield "b) Trojúhelník 10 Hz, rozsah 20 mV", fs, trojuhelnik, "mV", "line"

    fs = 128
    x = np.zeros(N)
    x[:128] = 1
    yield "c) Obdélníkový impuls 1 V, 128 vzorků", fs, x, "V", "step"
    x = np.zeros(N)
    x[:256] = 1
    yield "d) Obdélníkový impuls 1 V, 256 vzorků", fs, x, "V", "step"

    fs = 1024
    t = np.arange(N) / fs
    x = sum(
        amplituda * np.cos(2 * np.pi * frekvence * t)
        for amplituda, frekvence in zip((0.4, 0.3, 0.2, 0.1), (50, 100, 150, 200))
    )
    yield "e) Součet kosinusů 50, 100, 150 a 200 Hz", fs, x, "V", "line"

    fs = 64
    x = np.random.default_rng(42).uniform(-0.1, 0.1, N)
    yield "f) Rovnoměrný šum, 8 s, ±0,1 V", fs, x, "V", "line"
    x = np.zeros(N)
    x[63] = 64  # 64. vzorek pri cislovani od jedne
    yield "g) Diskrétní impuls 64 V v 64. vzorku", fs, x, "V", "stem"


def jednostranne_spektrum(x, fs):
    frekvence = np.fft.rfftfreq(N, d=1 / fs)
    amplitudy = np.abs(np.fft.rfft(x)) / N
    amplitudy[1:-1] *= 2  # DC a Nyquistova slozka se nezdvojuji
    return frekvence, amplitudy


def vykresli():
    fig, osy = plt.subplots(7, 2, figsize=(11.69, 16.54))  # A3 na vysku
    fig.suptitle("Signály a jejich jednostranná amplitudová spektra (N = 512)", fontsize=15)

    for (nazev, fs, x, jednotka, typ), (ax_signal, ax_spektrum) in zip(signaly(), osy):
        cas = np.arange(N) / fs
        if typ == "step":
            ax_signal.step(cas, x, where="post", linewidth=1.2)
        elif typ == "stem":
            ax_signal.vlines(cas[63], 0, x[63], linewidth=1.4)
            ax_signal.plot(cas[63], x[63], "o", markersize=3)
        else:
            ax_signal.plot(cas, x, linewidth=1)

        frekvence, amplitudy = jednostranne_spektrum(x, fs)
        ax_spektrum.plot(frekvence, amplitudy, linewidth=1)
        ax_signal.set(title=f"{nazev}  |  fs = {fs} Hz", xlabel="Čas [s]", ylabel=jednotka)
        ax_spektrum.set(title="Jednostranné amplitudové spektrum", xlabel="Frekvence [Hz]", ylabel=jednotka)
        ax_signal.set_xlim(0, N / fs)
        ax_spektrum.set_xlim(0, fs / 2)
        for ax in (ax_signal, ax_spektrum):
            ax.grid(True, alpha=0.35)
            ax.tick_params(labelsize=8)
            ax.title.set_fontsize(9)
            ax.xaxis.label.set_size(8)
            ax.yaxis.label.set_size(8)

    fig.subplots_adjust(left=0.075, right=0.975, top=0.955, bottom=0.045, hspace=0.94, wspace=0.25)
    VYSTUP.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(VYSTUP, format="pdf")
    plt.close(fig)
    print(f"PDF ulozeno do: {VYSTUP}")


if __name__ == "__main__":
    vykresli()
