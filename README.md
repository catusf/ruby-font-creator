

# Ruby Font Creator

Font creator to help students **learn and read foreign languages faster** by appending pronunciation or meaning to each glyph.

# Font Samplers

- This archive contains additional font files used in the samplers: [PinyinFonts.zip](https://github.com/catusf/ruby-font-creator/releases/download/v1.0/PinyinFonts.zip)


### Tigris-Pinyin-Bottom-Handwritten
- **Font file**: [Tigris-Pinyin-Bottom-Handwritten.ttf](output/Tigris-Pinyin-Bottom-Handwritten.ttf)

![Tigris-Pinyin-Bottom-Handwritten](output/Tigris-Pinyin-Bottom-Handwritten.png)

### Tigris-Pinyin-Left-Handwritten
- **Font file**: [Tigris-Pinyin-Left-Handwritten.ttf](output/Tigris-Pinyin-Left-Handwritten.ttf)

![Tigris-Pinyin-Left-Handwritten](output/Tigris-Pinyin-Left-Handwritten.png)

### Tigris-Pinyin-Top-Handwritten
- **Font file**: [Tigris-Pinyin-Top-Handwritten.ttf](output/Tigris-Pinyin-Top-Handwritten.ttf)

![Tigris-Pinyin-Top-Handwritten](output/Tigris-Pinyin-Top-Handwritten.png)

### Leo-Pinyin-Bottom-Serif
- **Font file**: [Leo-Pinyin-Bottom-Serif.ttf](output/Leo-Pinyin-Bottom-Serif.ttf)

![Leo-Pinyin-Bottom-Serif](output/Leo-Pinyin-Bottom-Serif.png)

### Leo-Pinyin-Left-Serif
- **Font file**: [Leo-Pinyin-Left-Serif.ttf](output/Leo-Pinyin-Left-Serif.ttf)

![Leo-Pinyin-Left-Serif](output/Leo-Pinyin-Left-Serif.png)

### Leo-Pinyin-Top-Serif
- **Font file**: [Leo-Pinyin-Top-Serif.ttf](output/Leo-Pinyin-Top-Serif.ttf)

![Leo-Pinyin-Top-Serif](output/Leo-Pinyin-Top-Serif.png)

### Onca-Pinyin-Bottom-Serif
- **Font file**: [Onca-Pinyin-Bottom-Serif.ttf](output/Onca-Pinyin-Bottom-Serif.ttf)

![Onca-Pinyin-Bottom-Serif](output/Onca-Pinyin-Bottom-Serif.png)

### Onca-Pinyin-Left-Serif
- **Font file**: [Onca-Pinyin-Left-Serif.ttf](output/Onca-Pinyin-Left-Serif.ttf)

![Onca-Pinyin-Left-Serif](output/Onca-Pinyin-Left-Serif.png)

### Onca-Pinyin-Top-Serif
- **Font file**: [Onca-Pinyin-Top-Serif.ttf](output/Onca-Pinyin-Top-Serif.ttf)

![Onca-Pinyin-Top-Serif](output/Onca-Pinyin-Top-Serif.png)

### Catus-Pinyin-Bottom-Sans
- **Font file**: [Catus-Pinyin-Bottom-Sans.ttf](output/Catus-Pinyin-Bottom-Sans.ttf)

![Catus-Pinyin-Bottom-Sans](output/Catus-Pinyin-Bottom-Sans.png)

### Catus-Pinyin-Left-Sans
- **Font file**: [Catus-Pinyin-Left-Sans.ttf](output/Catus-Pinyin-Left-Sans.ttf)

![Catus-Pinyin-Left-Sans](output/Catus-Pinyin-Left-Sans.png)

### Catus-Pinyin-Top-Sans
- **Font file**: [Catus-Pinyin-Top-Sans.ttf](output/Catus-Pinyin-Top-Sans.ttf)

![Catus-Pinyin-Top-Sans](output/Catus-Pinyin-Top-Sans.png)


### Features

| languages | preview | state | repository | base-font
| --- | :---: | :---: | --- | --- |
| Chinese | ![top](resources/tpl/annotation-top.png)  | **✔️** | [hanzi-pinyin-font](https://github.com/parlr/hanzi-pinyin-font/releases) | [DroidSansFallbackFull](https://github.com/parlr/platform_frameworks_base/blob/562c45cc841681ed80d4e94515b23c28eb60eae4/data/fonts/DroidSansFallbackFull.ttf)
| Tifinagh | -  | **🏃‍** | [hanzi-pinyin-font](https://github.com/parlr/tifinagh-font/releases) | [DroidSansFallbackFull](https://github.com/parlr/platform_frameworks_base/blob/562c45cc841681ed80d4e94515b23c28eb60eae4/data/fonts/DroidSansFallbackFull.ttf)
| :speaking_head: [request new one](https://github.com/parlr/ruby-font-creator/issues/new) | - | - | - | Please provide an open-source font |

**Legend:**
**⏸**→
**🏃‍**→
**✔️**




### Install

**Requirements**:  `nodejs`, [`yarn`](http://yarnpkg.com/) or [`npm`](http://npmjs.org/).

	yarn install

### Usage

**Requirements:** a `JSON` file describing _codepoint_-_glyph_-_gloss_ tuple (e.g.  [src/data.json](src/data.json)).

	yarn build

**Custom config:**

	yarn build --config ./src/config/default.js

**Custom data:**

	yarn build --data ./path-to/data.json

**Custom Font Name:**

	yarn build --font-name 'custom-font-name'

:information_source: maintenance tasks available are in the [makefile][./makefile], run `make` to see possible actions.

### Data Structure

A list of objects, each describing a glyph, with the following 3 elements:

1. a unicode `codepoint` ;
1. a base `glyph` ;
1. a `ruby` text.

Example:

	[
	  {
	    "codepoint": "U+03B1",
	    "glyph": "α",
	    "ruby": "alpha"
	  }
	]

### Font

This project use fonts under open-source licenses :
[DejaVuSans](https://github.com/TFTFonts/DejaVuSans),
[DroidSansFallbackFull](https://github.com/parlr/platform_frameworks_base/blob/562c45cc841681ed80d4e94515b23c28eb60eae4/data/fonts/DroidSansFallbackFull.ttf),
[Noto Sans CJK](https://github.com/nodebox/opentype.js/issues/273).


### License

> [Apache License 2.0](http://choosealicense.com/licenses/apache-2.0/)

### Contributors

* [Édouard Lopez](https://github.com/edouard-lopez/) ;
* [Hugo Lopez](https://github.com/hugolpz)
