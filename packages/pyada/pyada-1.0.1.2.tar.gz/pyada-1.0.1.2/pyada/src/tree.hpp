/*
 * Tree.h
 *
 *  Created on: Mar 24, 2015
 *      Author: Tadeze
 */

#ifndef TREE_H_
#define TREE_H_
#include "utility.hpp"
#include "globals.hpp"
#ifdef SERIALIZATION
#include "cereal/cereal.hpp"
#include "cereal/types/vector.hpp"
#include "cereal/types/memory.hpp"
#endif
#include <memory>
#include "feature_contribution.hpp"
namespace  osu {
    namespace ad {
        class Tree : public std::enable_shared_from_this<Tree> {
        private:
            std::shared_ptr<Tree> left_child_, right_child_, parent_;
            int node_size_, splitting_attribute_, depth_;
            double splitting_point_, min_attribute_val_, max_attribute_val_;
            int important_attribute_;
            std::shared_ptr<util::Dataset> make_dataset(std::vector<std::vector<double> > &data);

            int parent_id;
        public:
            int getParent_id() const;

            void setParent_id(int parent_id);


            const std::shared_ptr<Tree> &getLeftChild() const;

            const std::shared_ptr<Tree> &getRightChild() const;

            int node_size() const;

            void node_size(int nodeSize);

            int splitting_attribute() const;

            void splitting_attribute(int splittingAtt);

            int depth() const;

            void depth(int depth);

            double splitting_point() const;

            void splitting_point(double splittingPoint);

            double min_attribute_value() const;

            void min_attribute_value(double minAttVal);

            double max_attribute_value() const;

            void max_attribute_value(double maxAttVal);

            static bool range_check;

//    json trace_path(std::vector<double> &inst);
            Tree() : left_child_(nullptr), right_child_(nullptr), parent_(nullptr),
                     node_size_(0), splitting_attribute_(-1), depth_(0), splitting_point_(-9999), min_attribute_val_(0), max_attribute_val_(0),
                     important_attribute_(0){};

            virtual ~Tree() {};

            void
            iTree(const std::vector<int> &sample_index, const std::shared_ptr<util::Dataset> dataset, int height, int max_height,
                  bool stop_height, std::vector<int> const &column_index=std::vector<int>());

            void iTree(const std::vector<int>  &sample_index, std::vector<std::vector<double> > train_data, int height,
                       int max_height, bool stop_height,std::vector<int> const &column_index=std::vector<int>());

            double path_length(std::vector<double> &instance, bool check_missing_value = false);

          //Contribution
            contrib feature_contribution(std::vector<double> &instance) const;

            std::map<int, double> explanation(std::vector<double> &instance) const;
           // std::vector<int> allUsedAttributes(); TODO: Return all used attributes in a tree.
#ifdef SERIALIZATION
            // Serialization
            template<class Archive>
            void serialize(Archive &archive) {
                /*archive(cereal::make_nvp("nodesize",node_size_),cereal::make_nvp("depth_",depth_),
                        cereal::make_nvp("splitting_attribute_",splitting_attribute_),cereal::make_nvp("splitting_point_",splitting_point_),
                        cereal::make_nvp("min_attribute_val_",min_attribute_val_),cereal::make_nvp("max_attribute_val_",max_attribute_val_),
                        cereal::make_nvp("left_child_",left_child_),cereal::make_nvp("right_child_",right_child_)

                );*/
                archive(node_size_, depth_,
                        splitting_attribute_, splitting_point_,
                        min_attribute_val_, max_attribute_val_, left_child_, right_child_

                );
            }
#endif

        };
    }
}
#endif /* TREE_H_ */
