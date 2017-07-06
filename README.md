[![Build Status](https://travis-ci.org/parlr/ruby-font-creator.svg?branch=master)](https://travis-ci.org/parlr/ruby-font-creator)
[![Code Climate](https://codeclimate.com/github/parlr/ruby-font-creator/badges/gpa.svg)](https://codeclimate.com/github/parlr/ruby-font-creator)

# Ruby Font Creator

Font creator to help students **learn and read foreign languages faster** by appending pronunciation or meaning to each glyph.

### Features

| languages | preview | state | repository | base-font
| --- | :---: | :---: | --- | --- |
| Chinese | ![top](resources/tpl/annotation-top.png)  | **✔** | [hanzi-pinyin-font](https://github.com/parlr/hanzi-pinyin-font/releases) | [DroidSansFallbackFull](https://github.com/parlr/platform_frameworks_base/blob/562c45cc841681ed80d4e94515b23c28eb60eae4/data/fonts/DroidSansFallbackFull.ttf)
| :speaking_head: [request new one](https://github.com/parlr/ruby-font-creator/issues/new) | - | - | - | Please provide an open-source font |

**Legend:**
**✖**→
**★**→
**✔**


## Install

**Requirements**:  `nodejs`, [`yarn`](http://yarnpkg.com/) or [`npm`](http://npmjs.org/).

	yarn install

## Usage

**Requirements:** a `JSON` file describing _glyph_-_codepoint_-_pronunciation_ tuple (e.g.  [src/data.json](src/data.json)).

	yarn build

or specify the config filename to use (without extension):

	yarn build -- --config left-upward

**Custom data**:

	yarn build --  --data ./path-to/data.json

## Data Structure

A list of objects, each describing a glyph, with the following 3 elements:

1. a unicode `codepoint` ;
1. a base `glyph` ;
1. a `ruby` text.

Example:

	[
	  {
	    "codepoint": "U+03B1",
	    "ruby": "alpha",
	    "glyph": "α"
	  }
	]

## Font

This project use fonts under open-source licenses :
[DejaVuSans](https://github.com/TFTFonts/DejaVuSans),
[DroidSansFallbackFull](https://github.com/parlr/platform_frameworks_base/blob/562c45cc841681ed80d4e94515b23c28eb60eae4/data/fonts/DroidSansFallbackFull.ttf),
[Noto Sans CJK](https://github.com/nodebox/opentype.js/issues/273).


## License

> [Apache License 2.0](http://choosealicense.com/licenses/apache-2.0/)

## Contributors

* [Édouard Lopez](https://github.com/edouard-lopez/) ;
* [Hugo Lopez](https://github.com/hugolpz)
