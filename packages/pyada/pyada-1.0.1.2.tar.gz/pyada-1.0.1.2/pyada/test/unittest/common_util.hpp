//
// Created by tadeze on 4/4/17.
//

#ifndef PYIFOREST_COMMON_UTIL_HPP
#define PYIFOREST_COMMON_UTIL_HPP

#include <string>
#include <memory>

#include "utility.hpp"
using namespace osu::ad;
namespace common {
extern  std::string filename();
    std::shared_ptr<util::dataset> makeDataset(std::vector<std::vector<double> > &data);
}
#endif //PYIFOREST_COMMON_UTIL_HPP
