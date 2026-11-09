# Spektrální analýza signálů

Skript vygeneruje sedm signálů (a–g), spočítá jejich jednostranná amplitudová spektra a uloží všechny grafy na **jednu stránku PDF**. Každý signál má 512 vzorků. V levém sloupci jsou časové průběhy, v pravém spektra od 0 do `fs/2`.

## Spuštění

Je potřeba Python 3.13 a správce balíčků [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run python spektralni_analyza.py
```

Výsledek: [`output/pdf/spektra_signalu.pdf`](output/pdf/spektra_signalu.pdf).

Pokud už jsou balíčky `numpy` a `matplotlib` nainstalované v jiném prostředí, stačí spustit `python spektralni_analyza.py`.