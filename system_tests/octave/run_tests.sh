# generate code
itemc --generate-octave ../model/items/example.item || exit 1
# run tests
octave -p src-gen/ tests/demo.m
