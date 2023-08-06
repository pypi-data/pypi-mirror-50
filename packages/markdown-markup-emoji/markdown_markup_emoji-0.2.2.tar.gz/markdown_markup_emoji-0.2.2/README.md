# markdown_markup_emoji

[Python-Markdown][] extension for markup of Emoji in the markdown document.

Since it is marked up like `<span class="emoji">😃</span>`,
Make your Emoji bigger You can display it.

![build](https://travis-ci.org/EloiseSeverin/markdown_markup_emoji.svg?branch=master)

### Installation

Install with pip.

```
$ pip install markdown-markup-emoji
```

### Usage

It is used as an extension of [Python-Markdown][].

```.python
import markdown

md = markdown.Markdown(extensions=["markdown_markup_emoji.markup_emoji"])
md.convert("markdown text")
```

Or use from [Pelican][] as Markdown extension.

```.python
# pelicanconf.py
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        'markdown_markup_emoji.markup_emoji': {},
    },
    'output_format': 'html5',
}
```

### Add your style

Since it is marked up like `<span class="emoji">😃</span>`,
Add a style to be displayed with a bigger font.
<span style="font-size:180%">😃</span>

```.css
.emoji { font-size: 150%; }
```

### Notice

Since it does not include Emoji font, the display depends on OS.
For example, in Windows 7, pictograms may be displayed in black and white,
or may not be displayed.
Different Emoji may be displayed between iOS and Android.

[Unicode Full Emoji List][EmojiList] is here, please reference it.

[Python-Markdown]: https://github.com/Python-Markdown/markdown "Python-Markdown"
[Pelican]: https://blog.getpelican.com/ "Pelican Static Site Generator"
[EmojiList]: https://unicode.org/emoji/charts/full-emoji-list.html "Emoji List"
