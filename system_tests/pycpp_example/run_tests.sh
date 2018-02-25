# generate code
itemc --generate-python model/ImageData.item --src-gen-folder src-python || exit 1
itemc --generate-cpp    model/ImageData.item --src-gen-folder src-cpp || exit 1
# run tests
rm -rf data
mkdir data
cd src-python
jupyter nbconvert --to html --execute AlgoTestDataProvider.ipynb || exit 1
cd -

