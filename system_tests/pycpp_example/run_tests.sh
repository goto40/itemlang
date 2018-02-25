# generate code
itemc --generate-python model/ImageData.item --src-gen-folder src-python || exit 1
itemc --generate-cpp    model/ImageData.item --src-gen-folder src-cpp || exit 1
# run tests
cd src-python
#jupyter nbconvert --to notebook --execute AlgoTestDataProvider.ipynb || exit 1
jupyter nbconvert --to html --execute AlgoTestDataProvider.ipynb || exit 1
cd -

