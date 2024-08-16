rm -f build/svg/*

node --max_old_space_size=8192 --optimize_for_size --stack_size=4096 --require babel-core/register ./index.js --config=./src/config/bottom.js --data=src/data-org.json