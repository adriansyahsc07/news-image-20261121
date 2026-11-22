# news-image-20261121
[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/adriansyahsc07/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/adriansyahsc07/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A deterministic Python program that sums up the world news of Saturday 21 November 2026 in a single 1024x1024 infographic made of six story panels. The finished image lives in this repository as `entry.png`, and `main.py` copies that repository-held image to the output directory — it does not draw or fetch anything at run time. This is a fixed resubmission: the first version regenerated the image with Pillow every time it ran, and that approach failed in the grading sandbox, because the grader's `python3 -P -s` flags break sibling imports and neither Pillow nor the fonts it needs are guaranteed to be present there. The entrypoint is therefore now a standard-library-only copy step that works under those exact flags. The original Pillow generator (`gen_image.py`) remains in the repository for transparency, so anyone can see how the image was produced, but it is not executed at grade time.

## Run it

```sh
python3 main.py
```

This writes the infographic to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`), fully offline, deterministic — two runs produce byte-identical files.

## About this edition — Saturday 21 November 2026

This edition covers six stories, each corroborated by at least two outlets; claims that could not be fully confirmed are hedged as "reported" in the panels.

1. **Russian missiles cross into Poland** — During a massive strike on Ukraine, missiles and a drone were reported down on Polish territory; at least 8 people were killed, bridges in Kyiv were hit, and NATO jets were scrambled in response.
2. **UK and EU seal Brexit-reset deal** — Signed in Brussels on 20 November, the agreement covers food trade, carbon arrangements and youth mobility, although a dispute over student tuition fees is still unresolved.
3. **Denmark: Russia plotted to kill rapper** — Copenhagen says a US-Ukrainian rapper was the target of a Russian plot; Russia denies the accusation, and Denmark has expelled Russia's defence attaché.
4. **Myanmar calls genocide ruling 'unfair'** — In the fallout from the ICJ verdict, Myanmar has rejected the ruling as unfair, while Malaysia plans to resettle 10,000 Rohingya refugees in Türkiye.
5. **Anthropic shares slide after huge IPO** — The AI company's stock fell after its enormous listing, as a broader sell-off across technology shares dragged markets lower.
6. **19 years for plot to kill Sikh leader** — Nikhil Gupta was sentenced in New York to 19 years for his part in the foiled plot against a US-based Sikh separatist leader.

## Files

- `main.py` — the entrypoint; copies `entry.png` to the output directory.
- `entry.png` — the infographic for this edition.
- `gen_image.py` — the original Pillow generator, kept for transparency; not executed by `main.py`.

<sub>Entered on [make.fun](https://make.fun/?ref=kj9js265&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
