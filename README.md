# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/xuanyang667-boop/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/xuanyang667-boop/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image summing up the world's news of Friday 20 November 2026: Russia's
overnight barrage of 404 drones and 111 missiles on Kyiv, hitting three
bridges over the Dnipro, with two Russian missiles falling in Poland; the AI
sell-off sweeping Asia (Nikkei −4.8%, Kospi −5.2%) after Anthropic's record
IPO failed to revive faith in AI spending; the US widening its naval
blockade of Iran as Tehran masses tankers at Kharg Island; and briefs from
COP31's final day in Antalya, the PIF Tower hit in Riyadh, Estonia closing
its road borders with Russia, and Ukraine's Druzhba pipeline strike. Drawn
as a newspaper front page, "The World in One Image".

The program is `main.py` (Python 3.13, standard library only). It copies
the front page, `assets/entry.png`, to `/output/entry.png`. No network, no
randomness, no timestamps: two runs write byte-identical output. The image
is drawn by `make_image.py` (Pillow) from the day's reported news.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=hp6ck4g0&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
