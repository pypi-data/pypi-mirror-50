/*
 * utitlity.h
 *
 *  Created on: Mar 27, 2015
 *      Author: Tadeze
 */
#ifndef UTILITY_HPP_
#define UTILITY_HPP_

#include<iostream>
#include<fstream>
#include<sstream>
#include <cmath>
#include <cstdlib>
#include<ctime>
#include<algorithm>
#include<queue>
#include<string>
#include<iterator>
#include<vector>
#include<algorithm>
#include<map>
#include<set>
#include<random>
#include<utility>
#include <memory>
/*
#ifdef __linux__
#define SERIALIZATION
#endif
*/
namespace osu {
namespace ad {
namespace util {
using DoubleMatrix = std::vector<std::vector<double> >;
////default_random_engine gen(time(NULL));
struct Dataset {
	int ncol;
	int nrow;
	DoubleMatrix data;
	//std::vector<std::vector<double> > data;
	void print(int ix) {
		for (auto elem : data[ix])
			std::cout << elem << "\t";
	}
};

int rand_int(int min, int max);

int random_exclude(int min, int max, std::set<int> &exlude);

void sample_int(int min, int max, int nsample, std::vector<int> &sampleIndx);

double avg_pl(int n);

double rand_double(double min, double max);

//template<typename T>
double variance(std::vector<double> &x);

//template<typename T>
double mean(std::vector<double> points);

double tconf(std::vector<double> &points, double sigma);

std::vector<std::vector<double> > readcsv(const char *filename, char delim,
																					bool header);

extern std::ofstream log_file; //("log.txt");
std::map<double, double> ECDF(std::vector<double> points);

std::vector<double> AD_distance(const std::vector<std::vector<double> > &depths, bool weightToTail);

//log file
extern std::string tmpVar;

double score(double depth, int n);

//extern Data *dt;
extern std::string filename();

std::shared_ptr<util::Dataset> make_dataset(DoubleMatrix &data);

void display_vec(std::vector<double> &data);

std::vector<std::vector<double> > synthetic_data(int D, int N);

}

}
}
#endif
/* UTITLITY_H_ */

