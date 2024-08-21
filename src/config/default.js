import path from 'path'
// import layout from '../layouts'

export default {
  canvas: { width: 80, height: 80 },
  // dataSource: path.resolve('./src/data.json'),
  // get destFilename() {
  //   return path.resolve(`./build/${this.fontName}`)
  // },
  baseFontFilepath: path.resolve('./resources/fonts/NotoSansSC-Regular.ttf'),
  rubyFontFilepath: path.resolve('./resources/fonts/NotoSansMono-Regular.ttf'),
  fontName: 'Leo-Pinyin-Top',
  // formats: ['ttf'],
  // inputFiles: './build/**/*.svg',
  // workingDir: path.resolve('./build/svg'),
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
