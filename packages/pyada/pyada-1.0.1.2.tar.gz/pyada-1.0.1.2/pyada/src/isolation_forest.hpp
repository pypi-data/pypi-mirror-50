/*
 * IsolationForest.hpp
 *
 *  Created on: May 5, 2015
 *      Author: tadeze
 */

#ifndef ISOLATIONFOREST_HPP_
#define ISOLATIONFOREST_HPP_
#include "forest.hpp"

namespace osu {
	namespace ad {

		class IsolationForest : public Forest {
		public:
			IsolationForest()= default;

			IsolationForest(int num_trees, std::shared_ptr<util::Dataset> dataset,
							int num_sample, int max_height, bool stop_height, bool use_subsample,
							std::vector<int> const &column_index=std::vector<int>());

			void build_forest();
			virtual ~IsolationForest()= default;

			int adaptive_forest(double alpha, int stopLimit);

			void fixed_forest();

		};

	}
}
#ifdef SERIALIZATION
#include "cereal/types/polymorphic.hpp"
CEREAL_REGISTER_TYPE(osu::ad::IsolationForest);
CEREAL_REGISTER_POLYMORPHIC_RELATION(osu::ad::Forest, osu::ad::IsolationForest);
#endif
#endif /* ISOLATIONFOREST_HPP_ */
