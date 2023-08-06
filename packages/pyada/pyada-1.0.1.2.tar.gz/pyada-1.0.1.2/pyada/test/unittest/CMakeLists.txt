include_directories(${gtest_SOURCE_DIR}/include ${gtest_SOURCE_DIR})
add_executable(runIforestTests
        common_util.hpp test_tree.cpp  common_util.cpp test_utility.cpp
         test_Forest.cpp test_basiccheck.cpp )
#test_Forest.src
target_link_libraries(runIforestTests gtest gtest_main)
target_link_libraries(runIforestTests iforestlib)
#test_Forest.src test_FacadeForest.src

