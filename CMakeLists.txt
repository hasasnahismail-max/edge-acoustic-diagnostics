cmake_minimum_required(VERSION 3.10)
project(ZinoEADE)

# تعيين معيار C++ الحديث وسرعة التحسين القصوى
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3")

# تعريف الملف التنفيذي للنواة
add_executable(zino_eade main.cpp)
