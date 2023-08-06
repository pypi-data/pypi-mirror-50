//
// Created by zemichet on 3/30/16.
//

#include "facade_forest.hpp"
#ifdef  SERIALIZATION
#include <cereal/archives/json.hpp>
#include "cereal/archives/binary.hpp"
#endif

#include<cmath>
//using namespace osu::ad::;



std::shared_ptr<osu::ad::util::Dataset> make_dataset(osu::ad::util::DoubleMatrix &data) {
  /*
   * @param data: DoubleMatrix input data
   *
   */

  std::shared_ptr<osu::ad::util::Dataset> dt = std::make_shared<osu::ad::util::Dataset>();
  //auto dt = std::make_shared<util::Dataset>();
  dt->data = data;
  dt->ncol = (int) data[0].size();
  dt->nrow = (int) data.size();
  return dt;
}

//Check if the forest is built correctly
int osu::ad::FacadeForest::is_valid() const {

  if (forest_ == nullptr)
    return FOREST_NOT_TRAINED;

  //Check if test data is available
  if (test_dataset_ == nullptr || test_dataset_->nrow == 0)
    return NO_TEST_DATA;

  return OK;

}

int osu::ad::FacadeForest::train(util::DoubleMatrix &train_dataset,
												int num_tree, int num_sample, int max_height, bool rotate, bool adaptive,
												bool range_check, double rho, int stop_limit, std::vector<int> const &column_index) {

  num_trees_ = num_tree;
  num_sample_ = num_sample;
  rotate_ = rotate;
  max_height_ = max_height;
  adaptive_ = adaptive;
  range_check_ = range_check;
  rho_ = rho;
  stop_limit_ = stop_limit;

  bool use_subsample = num_sample_ != 0;
  bool stop_height = max_height_ != 0;
  train_dataset_ = make_dataset(train_dataset);

  if (!rotate_)
    forest_ = std::make_shared<osu::ad::IsolationForest>(num_trees_, train_dataset_,
                                            num_sample_, max_height_, stop_height, use_subsample, column_index); //build iForest
  else   // For now just use IsolationForest until changed.
    forest_ = std::make_shared<osu::ad::IsolationForest>(num_trees_, train_dataset_,
                                            num_sample_, max_height_, stop_height, use_subsample, column_index); //build iForest
  try {
    if (adaptive_)
     num_trees_ = forest_->adaptive_forest(rho_, stop_limit_);
    else
      forest_->fixed_forest();  //just for now build fixed tree
  } catch (std::exception &e) {
    std::cout << "Standard exception: " << e.what() << std::endl;
  }
  return num_trees_;  //Return number of trees_ used. Useful incase of adaptive_ tree growing
}

std::vector<double> osu::ad::FacadeForest::score(std::vector<std::vector<double> > &test_dataset, bool check_missing_value) {

  this->test_dataset_ = make_dataset(test_dataset);
  forest_->check_missing_value_ = check_missing_value;
  return forest_->anomaly_score(test_dataset_);
  //std::cout<<"Size of the data"<<_score.size();
  
}


std::vector<double> osu::ad::FacadeForest::anomaly_score() {

  //Make sure the forest is built and test data is available
  //is_valid();

  return forest_->anomaly_score(test_dataset_);

}

std::vector<std::vector<double> > osu::ad::FacadeForest::path_length() {
  /*  if(!is_valid())
        std::exit(1);
  */
  return forest_->path_length(test_dataset_);

}

std::vector<double> osu::ad::FacadeForest::average_depth() {
  /*if(!is_valid())
    std::exit(1);
  */
  std::vector<double> mean_depth(this->path_length().size());
  for (const auto &row : this->path_length()) {
    mean_depth.push_back(util::mean(row));
  }
  return mean_depth;
}

void osu::ad::FacadeForest::display_data(std::vector<std::vector<double> > &dataset) {
  auto df = make_dataset(dataset);
  std::cout << " Dimension of training data (" << df->nrow << ","
            << df->ncol << ")\n";
  for (const auto &row : df->data) {
    for (const auto &cell : row) {
      double ff = std::isnan(cell) ? -9999.0 : cell;
      std::cout << ff << "\t";
    }
    std::cout << "\n";
  }

}
std::map<int, double> osu::ad::FacadeForest::explanation(std::vector<double> &instance) {
	return forest_->importance(instance);
}

#ifdef SERIALIZATION
void osu::ad::FacadeForest::load(const std::string &file_name, bool binaryFormat) {
  std::ifstream file{file_name};
  if (!file.is_open()) {
    throw std::runtime_error{file_name + " could not be opened"};
  }
  if (binaryFormat) {
    cereal::BinaryInputArchive archive{file};

    archive(cereal::make_nvp("num_trees_", num_trees_), cereal::make_nvp("num_sample_", num_sample_),
            cereal::make_nvp("max_height_", max_height_), cereal::make_nvp("stop_limit_", stop_limit_),
            cereal::make_nvp("rho_", rho_), cereal::make_nvp("rotate_", rotate_),
            cereal::make_nvp("adaptive_", adaptive_), cereal::make_nvp("forest", forest_));
  } else {
    cereal::JSONInputArchive archive{file};
    archive(cereal::make_nvp("num_trees_", num_trees_), cereal::make_nvp("num_sample_", num_sample_),
            cereal::make_nvp("max_height_", max_height_), cereal::make_nvp("stop_limit_", stop_limit_),
            cereal::make_nvp("rho_", rho_), cereal::make_nvp("rotate_", rotate_),
            cereal::make_nvp("adaptive_", adaptive_), cereal::make_nvp("forest", forest_));

  }
}

void osu::ad::FacadeForest::save(const std::string &file_name, bool binaryFormat) {
  std::ofstream file{file_name};
  if (!file.is_open()) {
    throw std::runtime_error{file_name + " could not be opened"};
  }
  if (binaryFormat) {
    cereal::BinaryOutputArchive archive{file};

    archive(cereal::make_nvp("num_trees_", num_trees_), cereal::make_nvp("num_sample_", num_sample_),
            cereal::make_nvp("max_height_", max_height_), cereal::make_nvp("stop_limit_", stop_limit_),
            cereal::make_nvp("rho_", rho_), cereal::make_nvp("rotate_", rotate_),
            cereal::make_nvp("adaptive_", adaptive_), cereal::make_nvp("forest", forest_));
  } else {
    cereal::JSONOutputArchive archive{file};
    archive(cereal::make_nvp("num_trees_", num_trees_), cereal::make_nvp("num_sample_", num_sample_),
            cereal::make_nvp("max_height_", max_height_), cereal::make_nvp("stop_limit_", stop_limit_),
            cereal::make_nvp("rho_", rho_), cereal::make_nvp("rotate_", rotate_),
            cereal::make_nvp("adaptive_", adaptive_), cereal::make_nvp("forest", forest_));
  }

}
#else
void osu::ad::FacadeForest::save(const std::string &filename, bool binaryFormat){
    std::cerr<<"Save method is not defined in windows OS";
}
void osu::ad::FacadeForest::load(const std::string &filename, bool binaryFormat){
    std::cerr<<"Load method is not defined windows OS";
}
#endif



