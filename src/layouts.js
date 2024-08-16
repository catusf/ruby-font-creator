export default {
  ruby: {
    bottom: options => ({
      x: options.width / 2,
      y: options.height + 6,
      fontSize: 28,
      anchor: 'bottom center',
      attributes: { fill: 'black', stroke: 'black', id: 'ruby' }
    }),
    left: options => ({
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
    top: options => ({
      x: options.width / 2,
      y: -6,
      fontSize: 28,
      anchor: 'top center',
      attributes: { fill: 'black', stroke: 'black', id: 'ruby' }
    })
  },
  base: {
    bottom: options => ({
      x: options.width / 2,
      y: options.height - 14,
      fontSize: 56,
      anchor: 'bottom center',
      attributes: { fill: 'black', stroke: 'black', id: 'glyph' }
    }),
    right: options => ({
      x: options.width / 2 + 10,
      y: options.height,
      fontSize: 64,
      anchor: 'bottom center',
      attributes: { fill: 'black', stroke: 'black', id: 'glyph' }
    }),
    top: options => ({
      x: options.width / 2,
      y: 10,
      fontSize: 56,
      anchor: 'top center',
      attributes: { fill: 'black', stroke: 'black', id: 'glyph' }
    })
  }
}
