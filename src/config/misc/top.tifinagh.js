import path from 'path'
import layout from '../layouts'

export default {
  canvas: { width: 80, height: 80 },
  baseFontFilepath: path.resolve(
    './resources/fonts/NotoSans/NotoSansTifinagh-Regular.ttf'
  ),
  rubyFontFilepath: path.resolve(
    './resources/fonts/NotoSans/NotoSans-Regular.hinted.ttf'
  ),
  fontName: 'RFC-Tifinagh-regular',
  get layout() {
    return {
      base: layout.base.bottom(this.canvas),
      ruby: layout.ruby.top(this.canvas)
    }
  }
}
