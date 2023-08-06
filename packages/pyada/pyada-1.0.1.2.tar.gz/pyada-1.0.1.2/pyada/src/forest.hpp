/*
 * Forest.h
 *
 *  Created on: Aug 12, 2015
 *      Author: tadeze
 */

#ifndef FOREST_H_
#define FOREST_H_
#include <memory>
#include "tree.hpp"
namespace osu {
	namespace ad {

		class Forest {

		public:
			std::vector<std::shared_ptr<Tree> > trees_;
			int num_trees_;
			bool use_subsample_;
			int num_sample_;
			bool stop_height_;
			int max_height_;
			bool range_check_;
			bool check_missing_value_;
			std::vector<int> column_index_;
			std::shared_ptr<util::Dataset> dataframe_;

			//std::unique_ptr<util::Dataset> dataframe_;
			Forest() {
				use_subsample_ = false;
				num_trees_ = 0;
				num_sample_ = 256;
				dataframe_ = nullptr;
				check_missing_value_ = false;
			};

			Forest(int _ntree, std::shared_ptr<util::Dataset> dataset, int num_sample,
				   int max_height, bool stop_height, bool use_subsample,
				   std::vector<int> const &column_index= std::vector<int>()) {
				num_trees_ = _ntree;
				dataframe_ = dataset;
				num_sample_ = num_sample;
				stop_height_ = stop_height;
				max_height_ = max_height;
				use_subsample_ = use_subsample;
				if(column_index.empty())
					for(int i=0;i<dataset->ncol;i++)
						column_index_.push_back(i);
				else
					column_index_ = column_index;
			};

			virtual ~Forest()= default;


			double instance_score(std::vector<double> &instance);

			std::vector<double> anomaly_score(std::shared_ptr<util::Dataset> dataset);

			virtual std::vector<double> path_length(std::vector<double> &instance);

			std::vector<std::vector<double> > path_length(std::shared_ptr<util::Dataset> data);

			std::vector<double> meandepth();

			std::vector<double> ADtest(const std::vector<std::vector<double> > &pathlength, bool weighttotail);

			std::map<int, double> importance(std::vector<double> &instance);

			virtual double get_depth(std::vector<double> &instance, const std::shared_ptr<Tree> &tree);

			void get_sample(std::vector<int> &sample_index, int num_sample, bool use_subsample, int nrow);

			struct larger {
				bool operator()(const std::pair<int, double> p1, const std::pair<int, double> p2) {
					return p1.second < p2.second;
				}
			};

			/* virtual function for adaptive_ forest*/
			virtual int adaptive_forest(double alpha, int stopLimit) { return 0; };

			/*Fixed tree forest */
			virtual void fixed_forest() {};;

			/*
             * @input two vector v1 and
            * @return proporation of intersection ,[0,1]
            */

			double top_common_k(std::vector<int> &v1, std::vector<int> &v2) {
				std::vector<int> v3;
				std::sort(v1.begin(), v1.end());
				std::sort(v2.begin(), v2.end());
				std::set_intersection(v1.begin(), v1.end(), v2.begin(), v2.end(), back_inserter(v3));
				return (double) v3.size() / (double) v1.size();
			}

			void trace_path(std::vector<double> &inst, std::ostream &out);

			virtual std::vector<std::map<int, double> > feature_contrib(std::vector<double> &instance);
#ifdef SERIALIZATION
			// Serialization
			template<class Archive>
			void serialize(Archive &archive) {
				/*archive(cereal::make_nvp("num_trees_",num_trees_),cereal::make_nvp("num_sample_",num_sample_),
                        cereal::make_nvp("use_subsample_",use_subsample_),cereal::make_nvp("stop_height_",stop_height_),
                        cereal::make_nvp("trees_",trees_));*/
				archive(num_trees_, num_sample_, use_subsample_,
						stop_height_, trees_);

			}

#endif
		};
	}
}
#endif /* FOREST_H_ */
