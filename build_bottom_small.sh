rm -f build/svg/*

time node --max_old_space_size=8192 --optimize_for_size --stack_size=4096 --require babel-core/register ./index.js --config=./src/config/bottom.js --data=src/data-small-org.json --font-name=Pinyin-Test-Bottom-Small

python3 tools/font_stats.py build/Pinyin-Test-Bottom-Small.ttf --detailed
