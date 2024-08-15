rm -f build/svg/*

rm src/config/default.js
rm src/data.json

cp -f src/config/top.js src/config/default.js
cp -f src/data-small-org.json src/data.json

yarn build
