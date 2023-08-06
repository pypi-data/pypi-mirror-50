//
// Created by zemichet on 3/30/16.
//

#ifndef FacadeFOREST_HPP
#define FacadeFOREST_HPP
#ifdef __linux__
#define SERIALIZATION
#endif

#include "main.hpp"

namespace osu {
    namespace ad {
        class FacadeForest {
        private:
            int num_trees_;
            int num_sample_;
            int max_height_;
            bool rotate_;
            bool adaptive_;
            bool range_check_;
            double rho_;
            int stop_limit_;
            bool check_missing_value_;
            std::shared_ptr<util::Dataset> train_dataset_, test_dataset_;
            std::shared_ptr<Forest> forest_;

            const int FOREST_NOT_TRAINED = 1;
            const int NO_TEST_DATA = 2;
            const int OK = 0;

            //const int JSON_FORMAT=1;
            enum OUTPUT_FORMAT {
                JSON_FORMAT, BINARY_FORMAT
            };
        public:

            // enum FOREST{IFOREST,RFOREST,CFOREST};
            virtual ~FacadeForest() {};


					FacadeForest() {
						num_trees_ = 0;
						num_sample_ = 0;
						rotate_ = false;
						max_height_ = 0;
						adaptive_ = false;
						range_check_ = false;
						train_dataset_ = nullptr;
						test_dataset_ = nullptr;
						rho_ = 0.01;
						stop_limit_ = 0;
						forest_ = nullptr;

					}

            inline void trace_path(std::vector<double> &inst, std::ostream &out) {
              forest_->trace_path(inst, out);
            }

            int num_trees() const {
                return forest_->num_trees_;

            }

            int num_sample() const {
                return forest_->num_sample_;
            }

            int max_height() const {
                return forest_->max_height_;
            }


            bool adaptive() const {
                return this->adaptive_;
            }

            bool rotate() const {
                return rotate_;
            }

            bool range_check() const {
                return range_check_;
            }

            void range_check(bool rangecheck) {
                FacadeForest::range_check_ = rangecheck;
            }

            const std::shared_ptr<Forest> forest() const {
                return forest_;

            }

            const std::shared_ptr<util::Dataset> test_dataset() const {
                return test_dataset_;
            }

            const std::shared_ptr<util::Dataset> train_dataset() const {
                return train_dataset_;
            }

            //Methods

            int train(std::vector<std::vector<double> > &train_dataset, int num_tree,
											int num_sample, int max_height, bool rotate, bool adaptive,
											bool range_check, double rho, int stop_limit,
											std::vector<int> const &column_index = std::vector<int>());

            int train(std::vector<std::vector<double> > &train_dataset, int num_trees,
											int num_sample, int max_height, bool rotate) {
                return train(train_dataset, num_trees, num_sample, max_height, rotate, false, true, 0.01, 5);
            };


            std::vector<double> score(std::vector<std::vector<double> > &test_dataset, bool check_missing_value = false);


            std::vector<double> anomaly_score();

            std::vector<std::vector<double> > path_length();

            std::vector<double> average_depth();

            std::map<int, double> explanation(std::vector<double> &instance);

            void display_data(std::vector<std::vector<double> > &dataset);

            int is_valid() const;

            void load(const std::string &file_name, bool binaryFormat = true); //OUTPUT_FORMAT output_format);
            void save(const std::string &file_name, bool binaryFormat = true); //, OUTPUT_FORMAT output_format);

#ifdef SERIALIZATION

            template<class Archive>
            void serialize(Archive &archive) {

                /*archive(cereal::make_nvp("num_trees_",num_trees_),cereal::make_nvp("num_sample_",num_sample_),
                        cereal::make_nvp("max_height_",max_height_),cereal::make_nvp("stop_limit_",stop_limit_),
                        cereal::make_nvp("rho_",rho_),cereal::make_nvp("rotate_",rotate_),
                        cereal::make_nvp("adaptive_",adaptive_),cereal::make_nvp("forest",forest_));
                */
                archive(num_trees_, num_sample_, max_height_, stop_limit_,
                        rho_, rotate_, adaptive_, forest_);
            };
#endif

        };
    }
}
//CEREAL_REGISTER_TYPE(IsolationForest);
//CEREAL_REGISTER_POLYMORPHIC_RELATION(Forest,IsolationForest);

#endif //IFOREST_ADDIN_FacadeForest_HPP
