/*
 * IsolationForest.cpp
 *
 *  Created on: Mar, 2015
 *      Author: Tadeze
 */

#include "isolation_forest.hpp"
using namespace osu::ad;
struct smaller {
	bool operator()(const std::pair<int, double> p1, const std::pair<int, double> p2) {
		return p1.second > p2.second;
	}
};

IsolationForest::IsolationForest(int num_trees, std::shared_ptr<util::Dataset> dataset,
																 int num_sample, int max_height, bool stop_height, bool use_subsample,
																 std::vector<int> const &column_index)
		: Forest(num_trees, dataset, num_sample, max_height, stop_height, use_subsample, column_index) {

}
void IsolationForest::fixed_forest() {
	build_forest();
}
//Build forest using defined number of trees_

void IsolationForest::build_forest() {
	std::vector<int> sample_index;

	//build forest through all trees_
	for (int n = 0; n < this->num_trees_; n++) {

		//Sample and shuffle the data.
		sample_index.clear();
		get_sample(sample_index, num_sample_, use_subsample_, dataframe_->nrow);

		//build tree
		auto tree = std::make_shared<Tree>();
		tree->setParent_id(n);
		tree->iTree(sample_index, dataframe_, 0, max_height_, stop_height_, this->column_index_);
		this->trees_.push_back(tree); //add tree to forest
		//	Tree::treeIndx++;
	}

}

int IsolationForest::adaptive_forest(double alpha, int stopLimit) {
	//Build the RForest model
	double tk = ceil(alpha * 2 * dataframe_->nrow);
	std::vector<int> sampleIndex(this->num_sample_);
	// std::cout<<tk<<std::endl;
	//log_file<<"point,tree,x1,x2\n";
	bool converged = false;
	int convCounter = 0;
	int ntree = 0;
	std::vector<int> topKIndex;
	std::vector<int> prevTopKIndex;
	std::vector<double> totalDepth(dataframe_->nrow, 0);
	double prob = 0.0;
	std::priority_queue<std::pair<int, double>, std::vector<std::pair<int, double> >, larger> pq;
	std::shared_ptr<Tree> tree;
	while (!converged) {
		pq = std::priority_queue<std::pair<int, double>, std::vector<std::pair<int, double> >, larger>();

		//get sample data
		get_sample(sampleIndex, num_sample_, use_subsample_, dataframe_->nrow);

		//Fill the sampleIndex with indices of the sample rotated data
		tree = std::make_shared<Tree>();
		//    tree->range_check = this->rangecheck;
		tree->iTree(sampleIndex, dataframe_, 0, max_height_, stop_height_, this->column_index_);
		this->trees_.push_back(tree);
		ntree++;
		double d, dbar;
		topKIndex.clear();
		for (int inst = 0; inst < dataframe_->nrow; inst++) {
			d = this->get_depth(dataframe_->data[inst], tree);
			totalDepth[inst] += d;
			dbar = totalDepth[inst] / ntree;
			pq.push(std::pair<int, double>(inst, dbar));
		}
		//util::log_file<<num_trees_<<",";
		for (int i = 0; i < tk; i++) {
			topKIndex.push_back(pq.top().first);
			//  	util::log_file<<pq.top().first<<",";
			pq.pop();

		}

		if (ntree < 2) {
			prevTopKIndex = topKIndex;
//            util::log_file<<prob<<"\n";
			continue;
		}

		prob = top_common_k(topKIndex, prevTopKIndex);
		//util::log_file<<prob<<"\n";
		prevTopKIndex = topKIndex;
		if (prob == 1)
			convCounter++;
		else
			convCounter = 0;
		converged = convCounter > stopLimit;

		if (ntree < 50)
			converged = false;

	}

	return ntree;
}

