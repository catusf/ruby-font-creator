rm -f build/svg/*

rm src/config/default.js
rm src/data.json

cp src/config/top.js src/config/default.js
cp src/data-org.json src/data.json

yarn build
