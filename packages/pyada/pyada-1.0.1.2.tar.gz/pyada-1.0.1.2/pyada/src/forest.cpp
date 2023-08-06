/*
 * Forest.cpp
 *
 *  Created on: Aug 12, 2015
 *      Author: tadeze
 */

#include "forest.hpp"
using namespace osu::ad;
double Forest::get_depth(std::vector<double> &instance, const std::shared_ptr<Tree> &tree) {
    return tree->path_length(instance, this->check_missing_value_);
}


/*
 * Accepts single point (row) and return Anomaly Score
 */
double Forest::instance_score(std::vector<double> &instance) {

    double avgPathLength = util::mean(path_length(instance));
    double scores = pow(2, -avgPathLength / util::avg_pl(this->num_sample_));
    return scores;

}

/*
 * Score for  a set of dataframe_ in Dataset
 */
std::vector<double> Forest::anomaly_score(std::shared_ptr<util::Dataset> dataset) {
    std::vector<double> scores;
    //iterate through all points
    for (int inst = 0; inst < dataset->nrow; inst++) {
        scores.push_back(instance_score(dataset->data[inst]));
    }
    return scores;
}

/*
 * Trace path of a piont in a tree.
 */





/*
 * Return instance depth_ in all trees_
*/

std::vector<double> Forest::path_length(std::vector<double> &instance) {
    std::vector<double> depth;
       for(auto const &tree : this->trees_)
        depth.push_back(get_depth(instance, tree)); //#tree->path_length(instance,check_missing_value_));


    return depth;
}


/* PathLength for all points
*/
std::vector<std::vector<double> > Forest::path_length(std::shared_ptr<util::Dataset> data) {
    std::vector<std::vector<double> > depths;
    for (int r = 0; r < data->nrow; r++)
        depths.push_back(path_length(data->data[r]));
    return depths;
}

/* Compute the feature importance of a point
 * input: *inst data instance
 * output: feature importance
 * status: Incomplete!!
 */
std::map<int, double> Forest::importance(std::vector<double> &instance) {
    //Need to be re-implemented
    std::map<int, double> totalexplan;
    auto featureExplanation = Forest::feature_contrib(instance);
    for (const auto feature : featureExplanation) {
        for (auto explan : feature) {
            if (totalexplan.count(explan.first) > 0)
                totalexplan[explan.first] += explan.second;
            else
                totalexplan.insert(explan);
        }
    }

    return totalexplan;
}

//Sample data from the datset
void Forest::get_sample(std::vector<int> &sample_index, const int nsample, bool use_subsample, int nrow) {
    sample_index.clear();
    if (use_subsample && nsample < nrow)
      util::sample_int(0, nrow - 1, nsample, sample_index); //sample num_sample_
    else
      util::sample_int(0, nrow - 1, nrow, sample_index); //shuffle all index of the data

}


/*
 * Feature contribution
 */
    std::vector<std::map<int, double> > Forest::feature_contrib(std::vector<double> &instance) {
        // Iterate through all trees_ and collect their contributions

        std::vector<std::map<int, double> > contributions;
        for (auto &tree : this->trees_) {
            auto treeexplanation = tree->feature_contribution(instance).featureContribution();
            contributions.push_back(treeexplanation);
        }

        return contributions;
    }

void Forest::trace_path(std::vector<double> &inst, std::ostream &out){

    auto featureCont = Forest::feature_contrib(inst);
    for (const auto tree : this->trees_) {
        auto treePath = tree->feature_contribution(inst).contributions;
        for(auto feat : treePath) {
            out <<tree->getParent_id()<<","<<feat.first << "," << inst[feat.first]<<",[";
            for(auto depth_path: feat.second)
                out<<depth_path<<",";
            out<<"]";
            out<<"\n";
        }
    }

}

