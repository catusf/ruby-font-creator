rm -f build/svg/*

time node --max_old_space_size=8192 --optimize_for_size --stack_size=4096 --require babel-core/register ./index.js --config=./src/config/top.js --data=src/data-org.json --font-name=Leo-Pinyin-Top

python3 tools/font_stats.py build/Leo-Pinyin-Top.ttf --detailed