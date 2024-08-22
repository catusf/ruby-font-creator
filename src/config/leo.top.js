import path from 'path'

// Defaul option is Pinyins on top
export default {
  canvas: { width: 80, height: 80 },
  baseFontFilepath: path.resolve(
    './resources/fonts/LXGWWenKaiMono-Regular.ttf'
  ),
  rubyFontFilepath: path.resolve(
    './resources/fonts/LXGWWenKaiMono-Regular.ttf'
  ),
  fontName: 'Leo-Pinyin-Top-Serif',
  get layout() {
    return {
      base: this.baseLayout(this.canvas),
      ruby: this.rubyLayout(this.canvas)
    }
  },
  rubyLayout: options => ({
    x: options.width / 2,
    y: -6,
    fontSize: 28,
    anchor: 'top center',
    attributes: { fill: 'black', stroke: 'black', id: 'ruby' }
  }),
  baseLayout: options => ({
    x: options.width / 2,
    y: 19,
    fontSize: 60,
    anchor: 'top center',
    attributes: { fill: 'black', stroke: 'black', id: 'glyph' }
  })
}
