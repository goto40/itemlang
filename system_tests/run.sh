cd cpp
mkdir build
cd build
cmake -G Unix\ Makefiles .. && make && ./Tester.exe || exit 1
cd ..
exit 0
