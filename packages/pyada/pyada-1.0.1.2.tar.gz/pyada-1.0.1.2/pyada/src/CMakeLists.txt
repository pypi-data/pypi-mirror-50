project(pyiforest)
add_definitions(-std=c++11)
set(HEADER_FILES tree.hpp forest.hpp isolation_forest.hpp utility.hpp main.hpp facade_forest.hpp metric.hpp)
set(SOURCE_FILES tree.cpp forest.cpp isolation_forest.cpp utility.cpp facade_forest.cpp metric.cpp main.cpp stat/io_parser.cpp stat/io_parser.hpp feature_contribution.hpp log_writer.cpp log_writer.hpp
         command_parser.hpp command_parser.cpp globals.hpp bagged_forest.cpp bagged_forest.hpp)
#add_subdirectory(Eigen)
include_directories(include)
add_library(iforestlib STATIC ${SOURCE_FILES} ${HEADER_FILES})
