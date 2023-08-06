
# c++ interface to cython
from libcpp.vector cimport vector
from libcpp.map cimport map
from libcpp cimport bool
from libcpp.string cimport string

cdef extern from "src/facade_forest.hpp" namespace "osu::ad":
    cdef cppclass FacadeForest "osu::ad::FacadeForest":
        FacadeForest()
        void display_data(vector[vector[double]]&)
        int train(vector[vector[double]] &, int, int, int,
                        bool, bool, bool, double, int,vector[int]&)
        vector[double] score(vector[vector[double]] &, bool)
        vector[double]  anomaly_score()
        vector[vector[double]] path_length()
        vector[double] average_depth()
        int num_trees()
        int num_sample()
        int max_height()
        bool adaptive()
        bool range_check()
        bool rotate()
        int is_valid()
        void save(string, bool)
        void load(string, bool)
        map[int, double] explanation(vector[double] &)

cdef extern from "src/tree.hpp" namespace "osu::ad":
    cdef cppclass Tree "osu::ad::Tree":
        Tree()
        void iTree(vector[int] &, vector[vector[double]], int, int, bool, vector[int] &)
        double path_length(vector[double] &, bool)
        int maxTreeDepth()
        int node_size()
        int splitting_attribute()
        double splitting_point()
        int depth()
        double min_attribute_value()
        double max_attribute_value()
        map[int, double] explanation(vector[double] &)
