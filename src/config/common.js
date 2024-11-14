import path from 'path'

import layout from '../layouts'

export default {
  dataSource: path.resolve('./src/data.json'),
  // get destFilename() {
  //   return path.resolve(`./output/${this.fontName}`)
  // },
  formats: ['ttf'],
  inputFiles: './build/**/*.svg',
  workingDir: path.resolve('./build/svg')
}
