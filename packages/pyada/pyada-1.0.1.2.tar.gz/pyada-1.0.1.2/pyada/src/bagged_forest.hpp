//
// Created by tadeze on 1/10/18.
//

#ifndef PYIFOREST_BAGGED_FOREST_HPP
#define PYIFOREST_BAGGED_FOREST_HPP
#include "forest.hpp"

namespace osu {
namespace ad {
class BaggedForest : public Forest {
 public:
  BaggedForest() = default;
  BaggedForest(int _ntree, std::shared_ptr<util::Dataset> _df,
               int _nsample, int _maxheight, bool _stopheight, bool _rsample);
  void buidForest();
  virtual ~BaggedForest() = default;

  inline std::vector<int> findNAFeature(std::vector<double> &inst) {
    std::vector<int> naIndex;
    for (int i = 0; i < inst.size(); i++)
      if (std::isnan(inst[i]))
        naIndex.push_back(i);
    return naIndex;

  }
  int numberOfTreeUsed(std::vector<int> &inst);
  inline std::vector<int> getNoneNATrees(std::vector<double> &inst) {
    auto isNA = findNAFeature(inst);
    std::vector<int> trees;
    auto intersected = [](std::vector<int> x, std::vector<int> y) {
      std::vector<int> temp;
      for (auto ix : x)
        for (auto iy: y)
          if (ix == iy)return true;
      return false;
    };
    for (int i = 0; i < this->num_trees_; i++)
      if (!intersected(this->featureUsed[i], isNA))
        trees.push_back(i);
    return trees;

  }
  std::vector<double> path_length(std::vector<double> &inst) override;
 private:
  std::vector<std::vector<int> > featureUsed;
  int _numTreesUsed;

};
}
}

#endif //PYIFOREST_BAGGED_FOREST_HPP
