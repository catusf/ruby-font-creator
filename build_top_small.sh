rm -f build/svg/*

# time node --max_old_space_size=8192 --optimize_for_size --stack_size=4096 --require babel-core/register ./index.js --config=./src/config/default.js --data=src/data-small-org.json 
# time node --max_old_space_size=8192 --optimize_for_size --stack_size=4096 --require babel-core/register ./index.js --config=./src/config/left.js --data=src/data-small-org.json 
# time node --max_old_space_size=8192 --optimize_for_size --stack_size=4096 --require babel-core/register ./index.js --config=./src/config/top.leo.js --data=src/data-small-org.json 
time node --max_old_space_size=8192 --optimize_for_size --stack_size=4096 --require babel-core/register ./index.js --config=./src/config/onca.top.js --data=src/data-small-org.json 

# python3 tools/font_stats.py build/Pinyin-Test-Top-Small-Sans.ttf --detailed