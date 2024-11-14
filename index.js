import jsonfile from 'jsonfile'
import webfont from 'webfont'
import { argv } from 'yargs'






import helpers from './src/helpers'
import ruby from './src/ruby'
import svg from './src/svg'






function generateSvg(data, config) {
  const baseEngine = ruby.loadFont(config.baseFontFilepath)
  const rubyEngine = ruby.loadFont(config.rubyFontFilepath)
  const build_folder = `${config.workingDir}`

  const fs = require('fs');

  if (!fs.existsSync(build_folder)) {
    fs.mkdirSync(build_folder, { recursive: true });
    console.log(`Folder created: ${build_folder}`);
  } else {
    console.log(`Folder already exists: ${build_folder}`);
  }

  for (let datum = 0; datum < data.length; datum += 1) {
    const char = data[datum]
    const svgContent = svg.wrap(
      ruby.getBase(baseEngine, char.glyph, config.layout.base),
      ruby.getRuby(rubyEngine, char.ruby, config.layout.ruby)
    )

    const unicode = char.codepoint.replace('U+', 'u')
    svg.save(`${config.workingDir}/${unicode}-${char.glyph}.svg`, svgContent)
  }
}

function buildFont(config) {
  return webfont({
    files: config.inputFiles,
    fontName: config.fontName,
    startunicode: 0x3400
  })
    .then(content => content)
    .catch(err => console.log(err))
}

function start(cliArguments) {
  let config = helpers.setBuildConfig(cliArguments)
  config = helpers.setDataSource(config, cliArguments)
  config = helpers.setFontName(config, cliArguments)
  config = helpers.setBaseFontFilepath(config, cliArguments)
  config = helpers.setRubyFontFilepath(config, cliArguments)

  jsonfile.readFile(config.dataSource, (err, data) => {
    if (err) {
      throw err
    }

    helpers.prepare(config)
    generateSvg(data, config)

    buildFont(config).then(fontData =>
      helpers.generateFontFiles(fontData, config)
    )
  })
}

start(argv)
