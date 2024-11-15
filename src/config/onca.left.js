import path from 'path'
import layout from '../layouts'

export default {
  canvas: { width: 80, height: 80 },
  baseFontFilepath: path.resolve('./resources/fonts/NotoSerifSC-Regular.ttf'),
  rubyFontFilepath: path.resolve(
    './resources/fonts/LXGWWenKaiMono-Regular.ttf'
  ),
  fontName: 'Pinyin-Onca-Left-Serif',
  get layout() {
    return {
      base: this.baseLayout(this.canvas),
      ruby: this.rubyLayout(this.canvas)
    }
  },
  rubyLayout: options => ({
    x: -5,
    y: options.height / 2,
    fontSize: 24,
    anchor: 'top center',
    attributes: {
      fill: 'black',
      stroke: 'black',
      id: 'glyph',
      transform: `rotate(-1.5708, -5, ${options.height / 2})`
    }
  }),
  baseLayout: options => ({
    x: options.width / 2 + 10,
    y: options.height,
    fontSize: 64,
    anchor: 'bottom center',
    attributes: { fill: 'black', stroke: 'black', id: 'glyph' }
  })
}
