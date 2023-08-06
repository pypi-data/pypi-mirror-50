//
// Created by tadeze on 9/15/17.
//

#ifndef PYIFOREST_COMMANDPARSER_HPP
#define PYIFOREST_COMMANDPARSER_HPP
#include "utility.hpp"

class Parser{
public:
    std::string input_name;
    std::string output_name;
    std::string test_name;
    std::string metacols;
    int ntrees;
    int nsample;
    int maxdepth;
    bool header;
    bool adaptive;
    bool rotate;
    bool pathlength;
    bool range_check;
    bool miss_check;
    double precision;
    double alpha;
    int epoch;
    int seed;
    bool explain;
    bool oob;
    std::string savepath;
    std::string loadpath;
    bool help;
    void parse_argument(int argc, char* argv[]);
    Parser(){
        input_name = std::string();
        output_name = std::string();
        metacols = std::string();
        ntrees = 0;
        nsample = 0;
        pathlength = false;
        maxdepth = 0;
        header= true;
        miss_check=adaptive=rotate=range_check= false;
        savepath=loadpath=std::string();
    }
    void display_argument();
  osu::ad::util::DoubleMatrix readData(std::string input_file, bool header=true, std::string delimiter =",");

};
#endif //PYIFOREST_COMMANDPARSER_HPP
