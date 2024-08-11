import path from 'path'
import layout from '../layouts'

export default {
  canvas: { width: 80, height: 80 },
  dataSource: path.resolve('./src/data.json'),
  get destFilename() {
    return path.resolve(`./build/${this.fontName}`)
  },
  fontFilepath: path.resolve('./resources/fonts/DroidSansFallbackFull.ttf'),
  fontName: 'Droid-Sans-Top',
  formats: ['ttf'],
  inputFiles: './build/**/*.svg',
  workingDir: path.resolve('./build/svg'),
  get layout() {
    return {
      base: layout.base.bottom(this.canvas),
      annotation: layout.annotation.top(this.canvas)
    }
  }
}
