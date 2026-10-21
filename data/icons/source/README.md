# Icon source

`fcitx5-wetypex.png` is the full-bleed 1024 px master artwork. Do not edit the
files under `data/icons/hicolor` directly; change this image and regenerate the
installed icon set:

```sh
python3 tools/render_app_icons.py
```

The renderer applies the margins from the
[KDE Colorful Icons guidelines](https://develop.kde.org/hig/icons/colorful/)
and writes every size under `data/icons/hicolor`.
