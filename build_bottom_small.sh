rm -f build/svg/*

time node --max_old_space_size=8192 --optimize_for_size --stack_size=4096 --require babel-core/register ./index.js --config=./src/config/catus.bottom.js --data=src/data-small-org.json --font-name=Pinyin-Test-Bottom-Small --base-font=resources/fonts/NotoSerifSC-Regular.ttf --ruby-font=resources/fonts/LXGWWenKaiMono-Regular.ttf

python3 tools/font_stats.py build/Pinyin-Test-Bottom-Small.ttf --detailed
