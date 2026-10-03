cmake_minimum_required(VERSION 3.10)
project(ZinoEADE)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3")

# إضافة الملفات الهندسية للنواة ووحدة الذكاء الاصطناعي
add_executable(zino_eade main.cpp audio_processor.cpp eade_dsp.cpp)
