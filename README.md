# static

https://conf42.github.io/static/


## compress headshots

```sh
brew install pngquant
```

```sh
pngquant --quality=65-80 --force --ext .png headshots/*.png
```
## WebP versions (automatic)

conf42.com shows `headshots/<name>.webp` (500x400), `headshots/<name>.sm.webp` (160 px avatars)
and `podcasts/<name>.webp` (800 px) instead of the PNGs: 70-99% smaller. They're made by
`make_webp.py`, which the `webp` GitHub Action runs on every push that adds a PNG. Until the
WebP exists, the site falls back to the PNG, so uploading works exactly as before.
