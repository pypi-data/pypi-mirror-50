/*
 * Tree.cpp
 *
 *  Created on: Mar 24, 2015
 *      Author: Tadeze
 */
#include "tree.hpp"
#include "globals.hpp"
#include<stack>
#include<cmath>

bool osu::ad::Tree::range_check = false;
//double const MISSING_VALUE = -9999.0;
//int const NULL_TREE_CHILD_DEPTH = -999;

//std::ofstream util::log_file("log_file.log");
/*
 *@param data input data as double vector
 */
std::shared_ptr<osu::ad::util::Dataset> osu::ad::Tree::make_dataset(std::vector<std::vector<double> > &data) {
	std::shared_ptr<util::Dataset> dt = std::make_shared<util::Dataset>();//new util::Dataset();
	dt->data = data;
	dt->ncol = (int) data[0].size();
	dt->nrow = (int) data.size();
	return dt;
}

void osu::ad::Tree::iTree(std::vector<int> const &sample_index,
													std::vector<std::vector<double> > train_data,
													int height,
													int max_height,
													bool stop_height,
													std::vector<int> const &column_index) {
	std::shared_ptr<util::Dataset> dt = make_dataset(train_data);
	this->iTree(sample_index, dt, height, max_height, stop_height, column_index);
//   delete dt;
}



void osu::ad::Tree::iTree(std::vector<int> const &sample_index,
													const std::shared_ptr<osu::ad::util::Dataset> dataset,
													int height,
													int max_height,
													bool stop_height,
													std::vector<int> const &column_index) {
	depth_ = height;
	node_size_ = static_cast<int>(sample_index.size());
	if (sample_index.size() <= 1 || (stop_height && this->depth_ > max_height) || column_index.empty()) {
		return;
	}
	//*** Need modification
	//Initialize minmax array for holding max and min of an attributes

	std::vector<std::vector<double> > minmax;
	std::vector<double> tmp;

	//for (int j = 0; j < dataset->ncol; j++){
	for (int j : column_index) {
		//initialize max and min to random value
		tmp.push_back(dataset->data[sample_index[0]][j]);
		tmp.push_back(dataset->data[sample_index[0]][j]);
		minmax.push_back(tmp);
		tmp.clear();
	}

	//Compute max and min of each attribute
	for (int i : sample_index) {
		//vector<double> inst = data->data[i];
		for (int j : column_index) {
			if (dataset->data[i][j] < minmax[j].at(0))
				minmax[j].at(0) = dataset->data[i][j];
			if (dataset->data[i][j] > minmax.at(j).at(1))
				minmax[j].at(1) = dataset->data[i][j];
		}

	}

	//use only valid attributes
	std::vector<int> attributes;
	for (int j : column_index)
		if (minmax[j][0] < minmax[j][1])
			attributes.push_back(j);
	//return if no valid attribute found
	if (attributes.empty())
		return;

	// /Randomly pick an attribute and a split point

	this->splitting_attribute_ = attributes[util::rand_int(0, attributes.size() - 1)]; //randx];
	this->splitting_point_ =
			util::rand_double(minmax[this->splitting_attribute_][0], minmax[this->splitting_attribute_][1]);
	this->min_attribute_val_ = minmax[this->splitting_attribute_][0];
	this->max_attribute_val_ = minmax[this->splitting_attribute_][1];
	std::vector<int> left_node_data;
	std::vector<int> right_node_data;
	//Split the node into two
	for (int i : sample_index)
		if (dataset->data[i][splitting_attribute_] >= splitting_point_ &&
				(dataset->data[i][splitting_attribute_] != minmax[this->splitting_attribute_][0]))
			right_node_data.push_back(i);
		else
			left_node_data.push_back(i);

	left_child_ = std::make_shared<Tree>(); //new Tree(); //&dataL,height+1,max_height_);
	//left_child_->parent_ = this;
	left_child_->setParent_id(this->getParent_id());  // uniqualy identify each trees_.
	left_child_->iTree(left_node_data, dataset, this->depth_ + 1, max_height, stop_height);
	right_child_ = std::make_shared<Tree>();// new Tree(); //&dataR,height+1,max_height_);
	right_child_->setParent_id(this->getParent_id());

	//right_child_->parent_ = this;
	right_child_->iTree(right_node_data, dataset, this->depth_ + 1, max_height, stop_height);
}
//double splitting_value(){
//}

double osu::ad::Tree::path_length(std::vector<double> &instance, bool check_missing_value) {

	if (this->left_child_ == nullptr || this->right_child_ == nullptr) { ///referenced as null for some input data .
		return osu::ad::util::avg_pl(this->node_size_);
	}
	//Range check added
	double instance_attribute_value = instance[this->splitting_attribute_];

	if (Tree::range_check) {

		if (instance_attribute_value < this->min_attribute_val_
				&& osu::ad::util::rand_double(instance_attribute_value, this->min_attribute_val_) < this->min_attribute_val_)
			return 1.0;
		if (instance_attribute_value > this->min_attribute_val_
				&& osu::ad::util::rand_double(instance_attribute_value, this->max_attribute_val_) > this->max_attribute_val_)
			return 1.0;

	}

	//Checking missing data for the attribute.

	if (check_missing_value) {
		if (std::isnan(instance_attribute_value)) {

			auto left_child_size = (double) this->left_child_->node_size_ / (double) this->node_size_;
			double
					right_depth = (1.0 - left_child_size) * (this->right_child_->path_length(instance, check_missing_value) + 1.0);
			double left_depth = left_child_size * (this->left_child_->path_length(instance, check_missing_value) + 1.0);
			return right_depth + left_depth;
		}
	}

	if (instance_attribute_value >= this->splitting_point_)
		return this->right_child_->path_length(instance, check_missing_value) + 1.0;
	else
		return this->left_child_->path_length(instance, check_missing_value) + 1.0;
}


struct osu::ad::Contrib osu::ad::Tree::feature_contribution(std::vector<double> &instance) const {

	//Tree *root = this;
	auto root = this->shared_from_this();
	double instance_attribute_value;
	double depth = 0.0;
	Contrib contribution;
	while ((root->right_child_ != nullptr) || (root->left_child_ != nullptr)) {
		instance_attribute_value = instance[root->splitting_attribute_];

		//contributions[root->splitting_attribute_] = depth_ + util::avg_pl(root->node_size_);

		if (instance_attribute_value >= root->splitting_point_)
			root = root->right_child_;
		else
			root = root->left_child_;
		depth = depth + 1.0;
		if (root->splitting_attribute_ != -1)
			contribution.addcont(root->splitting_attribute_, depth + util::avg_pl(root->node_size_));
	}
	// depth_ = util::avg_pl(root->node_size_) + depth_;
	return contribution;//.feature_contribution();
}

std::map<int, double> osu::ad::Tree::explanation(std::vector<double> &instance) const {

	return feature_contribution(instance).featureContribution();

}
const std::shared_ptr<osu::ad::Tree> &osu::ad::Tree::getLeftChild() const {
	return left_child_;
}

const std::shared_ptr<osu::ad::Tree> &osu::ad::Tree::getRightChild() const {
	return right_child_;
}

int osu::ad::Tree::node_size() const {
	return node_size_;
}

void osu::ad::Tree::node_size(int nodeSize) {
	Tree::node_size_ = nodeSize;
}

int osu::ad::Tree::splitting_attribute() const {
	return splitting_attribute_;
}

void osu::ad::Tree::splitting_attribute(int splittingAtt) {
	Tree::splitting_attribute_ = splittingAtt;
}

int osu::ad::Tree::depth() const {
	return depth_;
}

void osu::ad::Tree::depth(int depth) {
	Tree::depth_ = depth;
}

double osu::ad::Tree::splitting_point() const {
	return splitting_point_;
}

void osu::ad::Tree::splitting_point(double splittingPoint) {
	Tree::splitting_point_ = splittingPoint;
}

double osu::ad::Tree::min_attribute_value() const {
	return min_attribute_val_;
}

void osu::ad::Tree::min_attribute_value(double minAttVal) {
	Tree::min_attribute_val_ = minAttVal;
}

double osu::ad::Tree::max_attribute_value() const {
	return max_attribute_val_;
}

void osu::ad::Tree::max_attribute_value(double maxAttVal) {
	Tree::max_attribute_val_ = maxAttVal;
}

int osu::ad::Tree::getParent_id() const {
	return parent_id;
}

void osu::ad::Tree::setParent_id(int parent_id) {
	Tree::parent_id = parent_id;
}

