import path from 'path'
import layout from '../layouts'

export default {
  canvas: { width: 80, height: 80 },
  baseFontFilepath: path.resolve('./resources/fonts/NotoSerifSC-Regular.ttf'),
  rubyFontFilepath: path.resolve(
    './resources/fonts/LXGWWenKaiMono-Regular.ttf'
  ),
  fontName: 'Pinyin-Onca-Bottom-Serif',
  get layout() {
    return {
      base: this.baseLayout(this.canvas),
      ruby: this.rubyLayout(this.canvas)
    }
  },
  rubyLayout: options => ({
    x: options.width / 2,
    y: options.height + 6,
    fontSize: 28,
    anchor: 'bottom center',
    attributes: { fill: 'black', stroke: 'black', id: 'ruby' }
  }),
  baseLayout: options => ({
    x: options.width / 2,
    y: options.height - 16,
    fontSize: 56,
    anchor: 'bottom center',
    attributes: { fill: 'black', stroke: 'black', id: 'glyph' }
  })
}
