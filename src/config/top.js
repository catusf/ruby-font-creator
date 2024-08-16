import path from 'path'
import layout from '../layouts'

export default {
  canvas: { width: 80, height: 80 },
  dataSource: path.resolve('./src/data.json'),
  get destFilename() {
    return path.resolve(`./build/${this.fontName}`)
  },
  baseFontFilepath: path.resolve('./resources/fonts/NotoSansSC-Regular.ttf'),
  rubyFontFilepath: path.resolve(
    './resources/fonts/NotoSansMono-Regular.ttf'
  ),
  fontName: 'Leo-Pinyin-Top',
  formats: ['ttf'],
  inputFiles: './build/**/*.svg',
  workingDir: path.resolve('./build/svg'),
  get layout() {
    return {
      base: layout.base.top(this.canvas),
      ruby: layout.ruby.top(this.canvas)
    }
  }
}
