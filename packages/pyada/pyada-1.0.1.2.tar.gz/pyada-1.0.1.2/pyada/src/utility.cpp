/*
 * utitlity.h
 *
 *  Created on: Mar 27, 2015
 *      Author: Tadeze
 */

#include "utility.hpp"

//default_random_engine gen(400);  //Debugging

std::default_random_engine gen(time(NULL));  //Production

double osu::ad::util::rand_double(double min, double max) {
	std::uniform_real_distribution<double> dist(min, max);
	return dist(gen);
}

int osu::ad::util::rand_int(int min, int max) {

	std::uniform_int_distribution<unsigned> dist(min, max);
	return dist(gen);
}

int osu::ad::util::random_exclude(int min, int max, std::set<int> &exlude) {
	int num = rand_int(min, max);
	return exlude.find(num) != exlude.end() ? random_exclude(min, max, exlude) : num;

}

void osu::ad::util::sample_int(int min, int max, int nsample, std::vector<int> &samples) {
	int count = 0;
	int rand_num;
	std::set<int> duplicate;
	while (count < nsample) {
		rand_num = random_exclude(min, max, duplicate);
		samples.push_back(rand_num);
		duplicate.insert(rand_num);
		count++;
	}

}

double osu::ad::util::avg_pl(int n) {

	return (((n - 1) <= 0) ?
			0.0 :
			((2.0 * (std::log((double) (n - 1)) + 0.5772156649))
					- (2.0 * (double) (n - 1)) / (1.0 + (double) (n - 1))));

}
double osu::ad::util::score(double depth, int n) {
	return std::pow(2, -depth / avg_pl(n));
}


double osu::ad::util::mean(std::vector<double> points) {
	auto sum = 0.0;
	for (double point : points)
		sum += point;
	return sum / (double) points.size();
}

double osu::ad::util::variance(std::vector<double> &x) {
	double sum = 0.0;
	double mn = mean(x);
	for (double elem : x) {
		sum += std::pow(elem - mn, 2);
	}
	return sum / (double) (x.size() - 1);
}

/* T-confidence interval
 *
 */
double osu::ad::util::tconf(std::vector<double> &points, double sigma = 0.95) {
	double sd = sqrt(variance(points));
	return 1.64 * sd / std::sqrt(points.size());
}

/*
 * Read csv file into vector,
 * used for testing
 */

std::vector<std::vector<double> > osu::ad::util::readcsv(const char *filename, char delim = ',',
																			bool header = true) {
	std::vector<std::vector<double> > values;
	std::vector<double> value_line;
	std::ifstream fin(filename);
	std::string item;
	if (header)  //if header available
		getline(fin, item);

	for (std::string line; getline(fin, line);) {
		std::istringstream in(line);
		while (getline(in, item, delim)) {
			value_line.push_back(std::atof(item.c_str()));
		}
		values.push_back(value_line);
		value_line.clear();
	}
	return values;
}

/*
 * Calculate the cumulative distribution function
 */
std::map<double, double> osu::ad::util::ECDF(std::vector<double> points) {

	std::map<double, double> cdf_value;
	sort(points.begin(), points.end());
	int j = -1;
	auto len = points.size();
	for (unsigned i = 0; i < points.size(); ++i) {
		if (i == 0 || points[i - 1] != points[i]) {
			j++;
			cdf_value.insert({points.at(i), static_cast<double>(i + 1) / len});
		} else {
			cdf_value[points.at(i)] = static_cast<double>(i + 1) / len;
		}
	}
	return cdf_value;

}

template<typename T>
std::vector<T> flatten(const std::vector<std::vector<T>> &v) {
	size_t total_size = 0;
	for (const auto &sub : v)
		total_size += sub.size();
	std::vector<T> result;
	result.reserve(total_size);
	for (const auto &sub : v)
		result.insert(result.end(), sub.begin(), sub.end());
	return result;
}

/*
 * Compute the Anderson-Darling distance for the depth_ distribution of each point
 * input: 2-d depth_ row X tree_depth
 * return 1-D score of each point
 */

std::vector<double> ADdistance(std::vector<std::vector<double> > depths, bool weightToTail =
false) {
	//flatten 2-d to 1-d and compute all_depth ECDF of using all points depths
	std::vector<double> all_depth = flatten(depths);
	std::map<double, double> Fxm = osu::ad::util::ECDF(all_depth); //all depth_ cdf

	std::vector<double> scores;
	/*
	 * compute score of each point
	 * sort the depth_, compute its ECDF
	 */
	for (std::vector<double> x : depths) {
		std::sort(x.begin(), x.end());
		std::map<double, double>::iterator iter = Fxm.begin();
		std::map<double, double> fxn = osu::ad::util::ECDF(x);  //empirical cdf of the point
		double val, sum = 0.0;
		for (double elem : x) {

			while (iter != Fxm.end()) {
				if (iter->first > elem) {

					val = (--iter)->second; //= ((i==0)?.0:(--iter)->second);
					break;
				}
				++iter;
			}
			if (iter == Fxm.end())
				val = 0.99999999; //close to 1 at the end of the distribution
			auto cdf_diff = std::max((fxn[elem] - val), 0.0);
			sum += weightToTail ? cdf_diff / sqrt(val) : cdf_diff; //distance of each point in the vector


		}
		scores.push_back(sum);
	}
	return scores;

}

std::string osu::ad::util::filename() {
	std::string file_name("/home/tadeze/projects/iForestCodes/pyiForest/test/unittest/synthetic5d34.csv");
	return file_name;
}

std::shared_ptr<osu::ad::util::Dataset> osu::ad::util::make_dataset(std::vector<std::vector<double> > &data) {
	std::shared_ptr<util::Dataset> dt = std::make_shared<util::Dataset>(); //new util::Dataset();
	dt->data = data;
	dt->ncol = (int) data[0].size();
	dt->nrow = (int) data.size();
	return dt;
}

void osu::ad::util::display_vec(std::vector<double> &data) {
	for (double row : data) {
		std::cout << row << "\t";
	}
};

std::vector<std::vector<double> > osu::ad::util::synthetic_data(int D, int N) {
	std::vector<std::vector<double> > data;

	for (int k = 0; k < N; k++) {
		std::vector<double> row;
		for (int j = 0; j < D; j++)
			row.push_back(util::rand_double(0, 2));
		data.push_back(row);
	}
	return data;
}







/* UTITLITY_H_ */

