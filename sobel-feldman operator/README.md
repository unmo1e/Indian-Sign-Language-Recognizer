g++ src/main.cpp src/stb_image.c src/stb_image_write.c -o main -Isrc -std=c++11 -g ; gdb -ex=run -ex=bt -ex=quit --args ./main input.jpg output.jpg
