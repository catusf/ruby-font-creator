import test from 'ava'

import layout from '../src/layouts'

test('verify layout.ruby.top attributes', t => {
  const svgAttributes = layout.ruby.top({ width: 80, height: 80 })

  t.truthy(svgAttributes.x)
  t.truthy(svgAttributes.y)
  t.truthy(svgAttributes.fontSize)
  t.truthy(svgAttributes.anchor)
  t.deepEqual(svgAttributes.attributes, {
    id: 'ruby',
    fill: 'black',
    stroke: 'black'
  })
})

test('verify layout.base.bottom attributes', t => {
  const svgAttributes = layout.base.bottom({ width: 80, height: 80 })

  t.truthy(svgAttributes.x)
  t.truthy(svgAttributes.y)
  t.truthy(svgAttributes.fontSize)
  t.truthy(svgAttributes.anchor)
  t.deepEqual(svgAttributes.attributes, {
    id: 'glyph',
    fill: 'black',
    stroke: 'black'
  })
})
