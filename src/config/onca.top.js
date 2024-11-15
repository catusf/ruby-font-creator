import path from 'path'

// Defaul option is Pinyins on top
export default {
  canvas: { width: 80, height: 80 },
  baseFontFilepath: path.resolve('./resources/fonts/NotoSerifSC-Regular.ttf'),
  rubyFontFilepath: path.resolve(
    './resources/fonts/LXGWWenKaiMono-Regular.ttf'
  ),
  fontName: 'Pinyin-Onca-Top-Serif',
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
    y: 10,
    fontSize: 56,
    anchor: 'top center',
    attributes: { fill: 'black', stroke: 'black', id: 'glyph' }
  })
}
