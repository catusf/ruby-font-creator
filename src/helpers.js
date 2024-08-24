import fs from 'fs'
import path from 'path'
import mkdirp from 'mkdirp'

export default {
  setCommonConfig(config) {
    const common_config = require(path.resolve('./src/config/common.js'))
      .default // eslint-disable-line global-require, import/no-dynamic-require
    const newConfig = Object.assign({}, config)

    // Copy config from common_config to newconfig
    return newConfig
  },

  setFontName(config, cliArguments) {
    const newConfig = Object.assign({}, config)

    if (cliArguments.fontName) {
      newConfig.fontName = cliArguments.fontName
    }

    return newConfig
  },

  setBaseFontFilepath(config, cliArguments) {
    const newConfig = Object.assign({}, config)

    if (cliArguments.baseFont) {
      newConfig.baseFontFilepath = path.resolve(cliArguments.baseFont)
    }

    return newConfig
  },

  setRubyFontFilepath(config, cliArguments) {
    const newConfig = Object.assign({}, config)

    if (cliArguments.rubyFont) {
      newConfig.rubyFontFilepath = path.resolve(cliArguments.rubyFont)
    }

    return newConfig
  },

  setDataSource(config, cliArguments) {
    const newConfig = Object.assign({}, config)

    if (cliArguments.data) {
      newConfig.dataSource = path.resolve(cliArguments.data)
    }

    return newConfig
  },

  setBuildConfig(cliArguments) {
    let config = require(path.resolve('./src/config/default.js')).default // eslint-disable-line global-require, import/no-dynamic-require

    if (cliArguments.config) {
      config = require(path.resolve(`${cliArguments.config}`)).default // eslint-disable-line global-require, import/no-dynamic-require
    }

    const common_config = require(path.resolve('./src/config/common.js'))
      .default // eslint-disable-line global-require, import/no-dynamic-require
    const newConfig = Object.assign({}, config, common_config)

    return newConfig
  },
  prepare(config) {
    try {
      return fs.mkdirSync(config.workingDir).resolve()
    } catch (error) {
      return Promise.resolve(new Error(error))
    }
  },
  writeFont(content, destination) {
    try {
      return fs.writeFileSync(destination, content).resolve()
    } catch (error) {
      return Promise.resolve(new Error(error))
    }
  },
  generateFontFiles(content, config) {
    const self = this

    return new Promise((resolve, reject) => {
      // eslint-disable-next-line func-names
      config.formats.map(format => {
        const directoryPath = path.resolve(`./output`)
        const filePath = `${directoryPath}/${config.fontName}.${format}`

        return self
          .writeFont(content[format], filePath)
          .then(() => console.log(`wrote: ${filePath}`))
          .catch(err => {
            reject()
            console.error(`failed to write ${filePath}`, err)
          })
      })
      resolve()
    })
  }
}
