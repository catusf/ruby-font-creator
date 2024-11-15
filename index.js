import jsonfile from 'jsonfile'
import webfont from 'webfont'
import { argv, showCompletionScript } from 'yargs'














import helpers from './src/helpers'
import ruby from './src/ruby'
import svg from './src/svg'














function generateSvg(data, config) {
  const baseEngine = ruby.loadFont(config.baseFontFilepath)
  const rubyEngine = ruby.loadFont(config.rubyFontFilepath)
  const build_folder = `${config.workingDir}`

  const fs = require('fs')

  if (!fs.existsSync(build_folder)) {
    fs.mkdirSync(build_folder, { recursive: true })
    console.log(`Folder created: ${build_folder}`)
  } else {
    console.log(`Folder already exists: ${build_folder}`)
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

// Function to extract value of --config
function getConfigValue(args) {
  const configArg = args.find(arg => arg.startsWith('--config='))
  if (configArg) {
    // Extract value after the '=' sign
    return configArg.split('=')[1]
  }
  return null // Return null if --config is not found
}

// Modify the filename to use .json instead of .js, or return 'default.json' if no config found
function getConfigData(configValue) {
  if (configValue) {
    // Replace .js extension with .json
    return configValue.replace('.js', '.json')
  }
  // Return 'default.json' if no config file is found
  return 'default.json'
}

function start(cliArguments) {
  let config = helpers.setBuildConfig(cliArguments)
  config = helpers.setDataSource(config, cliArguments)
  config = helpers.setFontName(config, cliArguments)
  config = helpers.setBaseFontFilepath(config, cliArguments)
  config = helpers.setRubyFontFilepath(config, cliArguments)

  const args = process.argv

  const config_value = getConfigValue(args)
  const config_data_file = getConfigData(config_value)

  // Convert the object to a JSON string
  const jsonData = JSON.stringify(config, null, 2)

  const fs = require('fs')

  // Write the JSON string to a file synchronously
  try {
    fs.writeFileSync(config_data_file, jsonData)
    console.log('Data has been saved to data.json')
  } catch (err) {
    console.log('Error writing to file:', err)
  }

  // Log the entire arguments array
  // console.log(args)

  jsonfile.readFile(config.dataSource, (err, data) => {
    if (err) {
      throw err
    }

    helpers.prepare(config)

    // Use when only generate the config then quit
    // console.log(cliArguments)
    
    if (cliArguments.save_config) {
      console.log(`Save ${cliArguments.config} then quits.`)
      return
    }
    
    generateSvg(data, config)

    buildFont(config).then(fontData =>
      helpers.generateFontFiles(fontData, config)
    )
  })
}

start(argv)
