//
// Created by tadeze on 4/4/17.
//

#include "common_util.hpp"

 std::string common::filename() {
     std::string filename("synth2d.dt");
    return filename;
    }

std::shared_ptr<util::dataset> common::makeDataset(std::vector<std::vector<double> > &data) {
    std::shared_ptr<util::dataset> dt = std::shared_ptr<util::dataset>(new util::dataset());
    dt->data = data;
    dt->ncol = (int)data[0].size();
    dt->nrow = (int)data.size();
    return dt;
}
