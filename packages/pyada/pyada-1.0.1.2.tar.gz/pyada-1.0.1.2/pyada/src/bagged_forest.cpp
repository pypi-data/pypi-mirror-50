
#include "bagged_forest.hpp"
#include<cmath>
//using namespace osu::ad;


void osu::ad::BaggedForest::buidForest() {

    std::vector<int> sample_index;
    std::vector<int> sample_column;
    //build forest through all trees_
    auto reduced_dim = static_cast<int>(std::ceil(dataframe_->ncol / sqrt(dataframe_->ncol))); // Subset of the dimension.
    for (int n = 0; n < this->num_trees_; n++) {

        //Sample and shuffle the data.
        sample_index.clear();
        sample_column.clear();
        get_sample(sample_index, num_sample_, use_subsample_, dataframe_->nrow);
        get_sample(sample_column, reduced_dim, true, dataframe_->ncol);

        this->featureUsed.push_back(sample_column);
        //build tree
        auto tree = std::make_shared<Tree>();
        tree->setParent_id(n);
        //	tree->range_check = this->rangecheck;
        tree->iTree(sample_index,dataframe_, 0, max_height_, stop_height_,sample_column);
        this->trees_.push_back(tree); //add tree to forest
        //	Tree::treeIndx++;
    }


}
std::vector<double>  osu::ad::BaggedForest::path_length(std::vector<double> &inst)  {

    auto trees_without_NA = this->getNoneNATrees(inst);
    std::vector<double> depth(trees_without_NA.size());
    for(int i : trees_without_NA) {

        depth.push_back(this->get_depth(inst, this->trees_[i]));
    }
    _numTreesUsed = static_cast<int>(depth.size());

    return depth;
}
int osu::ad::BaggedForest::numberOfTreeUsed(std::vector<int> &inst) {
    return _numTreesUsed;
}

osu::ad::BaggedForest::BaggedForest(int _ntree, std::shared_ptr<util::Dataset> _df, int _nsample, int _maxheight,
                           bool _stopheight, bool _rsample):Forest(_ntree, _df,_nsample,_maxheight,_stopheight,_rsample){


}

