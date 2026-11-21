# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/adriansyahsc07/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/adriansyahsc07/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A deterministic Python program that sums up the world news of Saturday 21 November 2026 in a single 1024x1024 infographic: six panels, one per story, each with a category tag, a headline, a line or two of context and a motif drawn with Pillow primitives, so the picture explains itself without a news feed.

## Run it

```sh
python3 main.py
```

This writes the infographic to `/output/entry.png`. The program runs
fully offline and is deterministic — two runs produce byte-identical
PNG files.

---

<sub>Entered on [make.fun](https://make.fun/?ref=kj9js265&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>

## About this edition — Saturday 21 November 2026

The six stories, each corroborated by at least two outlets before it
was drawn (unconfirmed claims are hedged as "reported" in the image):

1. **Russian missiles cross into Poland** — missiles and a drone
   reported down in Poland during a huge strike on Ukraine; at least 8
   killed, Kyiv bridges hit, NATO jets scrambled. *(Helsinki Times,
   BBC, GeoBrowser roundup)*
2. **UK and EU seal Brexit-reset deal** — signed in Brussels on 20 Nov:
   food trade, carbon and youth-mobility arrangements; a row over
   student tuition fees remains open. *(Helsinki Times, GeoBrowser)*
3. **Denmark: Russia plotted to kill rapper** — Copenhagen says a
   US-Ukrainian rapper was the target; Russia denies it and Denmark
   expels Russia's defence attaché. *(BBC, News Media House)*
4. **Myanmar calls genocide ruling 'unfair'** — fallout from the ICJ
   verdict: Malaysia plans to resettle 10,000 Rohingya refugees in
   Türkiye. *(BBC/NYT/Al Jazeera roundups, Daily Jagran)*
5. **Anthropic shares slide after huge IPO** — the AI firm's stock
   falls as a wider tech sell-off drags markets down. *(BBC, school-
   assembly news roundups)*
6. **19 years for plot to kill Sikh leader** — Nikhil Gupta sentenced
   in New York for the foiled plot against a US-based Sikh separatist
   leader. *(GeoBrowser, BBC)*

## Files

- `main.py` — entrypoint; writes `/output/entry.png`.
- `gen_image.py` — the Pillow infographic generator (layout, text
  wrapping and all six drawn motifs).
- `entry.png` — the generated image for this edition.
