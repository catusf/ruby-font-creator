import jsonfile from 'jsonfile'
import webfont from 'webfont'
import { argv } from 'yargs'































import helpers from './src/helpers'
import ruby from './src/ruby'
import svg from './src/svg'




















const fs = require('fs');












function generateSvg(data, config) {
  const baseEngine = ruby.loadFont(config.baseFontFilepath)
  const rubyEngine = ruby.loadFont(config.rubyFontFilepath)
  const build_folder = `${config.workingDir}`

  // Define the codepoint you're searching for
  const targetCodePoint = "U+1ED9";

  const fs = require('fs')

  if (!fs.existsSync(build_folder)) {
    fs.mkdirSync(build_folder, { recursive: true })
    console.log(`Folder created: ${build_folder}`)
  } else {
    console.log(`Folder already exists: ${build_folder}`)
  }

  for (let datum = 0; datum < data.length; datum += 1) {
    const char = data[datum]

    const unicode = char.codepoint.replace('U+', 'u')
    if (!char.ruby){ 
      const svgContent = svg.wrap(
        ruby.getBase(baseEngine, char.glyph, config.layout.norm)
      )
      svg.save(`${config.workingDir}/${unicode}-${char.glyph}.svg`, svgContent)
    }
    else {
      const svgContent = svg.wrap(
        ruby.getBase(baseEngine, char.glyph, config.layout.base),
        ruby.getRuby(rubyEngine, char.ruby, config.layout.ruby)
      )
      svg.save(`${config.workingDir}/${unicode}-${char.glyph}.svg`, svgContent)
    }




    // svg.save(`${config.workingDir}/${unicode}.svg`, svgContent)
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


// Function to load the code points from the JSON file
function loadExtraCodePoints() {
  const data = fs.readFileSync('src/added_codepoints.json', 'utf-8');
  return JSON.parse(data);
}
// Function to add code points to the existing data
function addCodePointsToExistingData(codePoints, existingData) {
  codePoints.forEach(codePoint => {
    // Convert the code point (e.g., "U+6211") to the actual character
    const character = String.fromCodePoint(parseInt(codePoint.replace('U+', ''), 16)); // Remove 'U+' and convert to number

    // Add new object to the existing array
    existingData.push({
      codepoint: codePoint,
      ruby: "",  // Ruby is set to an empty string
      glyph: character  // Glyph is the character corresponding to the code point
    });
  });

  // Write the updated array back to the file
  // fs.writeFileSync('existingData.json', JSON.stringify(existingData, null, 2));

  // console.log('Updated data written to existingData.json');
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
    console.log('Data has been saved to ' + config_data_file)
  } catch (err) {
    console.log('Error writing to file:', err)
  }

  // Log the entire arguments array
  // console.log(args)

  jsonfile.readFile(config.dataSource, (err, data) => {
    if (err) {
      throw err
    }

    // Example usage
    const extra_data = loadExtraCodePoints();
    
    addCodePointsToExistingData(extra_data, data);

    helpers.prepare(config)

    // Use when only generate the config then quit
    // return

    generateSvg(data, config)

    buildFont(config).then(fontData =>
      helpers.generateFontFiles(fontData, config)
    )
  })
}

/*
// Define the Unicode ranges in an array
const unicodeRanges = [
  { start: 0x0000, end: 0x007F }, // Basic Latin
  { start: 0x0080, end: 0x00FF }, // Latin-1 Supplement
  { start: 0x0100, end: 0x017F }, // Latin Extended-A
  { start: 0x0180, end: 0x024F }, // Latin Extended-B
  { start: 0x1E00, end: 0x1EFF }, // Latin Extended Additional
  { start: 0x0300, end: 0x036F }, // Combining Diacritical Marks
];


// Function to generate code points in the specified ranges
function generateUnicodeCodePoints(ranges) {
  const codePoints = [];
  
  ranges.forEach(range => {
    for (let i = range.start; i <= range.end; i++) {
      codePoints.push(`U+${i.toString(16).toUpperCase().padStart(4, '0')}`);
    }
  });

  return codePoints;
}

// Generate the Unicode code points array
const codePoints = generateUnicodeCodePoints(unicodeRanges);

// Write the code points to a JSON file
fs.writeFileSync('src/added_codepoints.json', JSON.stringify(codePoints, null, 2));

console.log('Unicode code points written to unicodeCodePoints.json');

*/

start(argv)
