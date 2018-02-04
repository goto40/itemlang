# run tests
itemc --generate-octave ../model/items/example.item || exit 1

octave -p src-gen/ tests/demo.m
