#ifndef METRIC_HPP_
#define METRIC_HPP_
//#include "utility.hpp"
#include <vector>
 #include <algorithm>
 #include <iostream>
 #include <cmath>

namespace metric {



//Area under ROC curve
double AUC(std::vector<double> &labels, std::vector<double> &scores,int n,int posclass);
//Average precision
//double ap(std::vector<double> &labels, std::vector<double> &scores,int n,int posclass);
double add(double a , double b);
}


#endif
