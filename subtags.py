from GlotScript import sp

sp('これは日本人です')
# ('Hira', 0.625, {'details': {'Hira': 0.625, 'Hani': 0.375}, 'tie': False, 'interval': 0.25})


print(sp('e')[:1])
# ('Latn', 1.0)

print(sp('මේක සිංහල')[0])
# 'Sinh'
