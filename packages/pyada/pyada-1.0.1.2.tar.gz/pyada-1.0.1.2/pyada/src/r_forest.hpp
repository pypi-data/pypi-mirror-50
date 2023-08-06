/*
 * RotationForest.hpp
 *
 *  Created on: Aug 26 2015
 *      Author: tadeze
 */
/*struct _doubleframe 
 {
 double** dt;
 int nrow;
 int ncol;

 };
 typedef struct _doubleframe doubleframe;

 */

#ifndef RFOREST_H_
#define RFOREST_H_
#include "Eigen/Dense"
#include "Eigen/QR"
#include "forest.hpp"
//#include "cincl.hpp"
using namespace util;
class RForest: public Forest {
 

 	std::vector<Eigen::MatrixXd> rotMatrices;
   	std::mt19937 eng{std::random_device{}()}; //For production
  	//std::default_random_engine eng;   //for debugging


public:
//Constructor
	RForest(int _ntree,dataset* _df,int _nsample,int _maxheight,
			bool _stopheight,bool _rsample) :
			Forest(_ntree, _df, _nsample, _maxheight, _stopheight, _rsample) {
       // 	eng.seed(time(NULL));  //initialize random generator seed .
	//	eng.seed(400); //For debugging 
            };

	RForest() {};
	~RForest() {};


//Methods
 	void convertToDf(Eigen::MatrixXd &m, dataset* df);
	void rotateInstance(std::vector<double> &inst, Eigen::MatrixXd &m,double* rotatedData);
	void buildForest(dataset* df);
	void generateRandomRotationMatrix(Eigen::MatrixXd& M, int n );
	void convertToVector(Eigen::MatrixXd &m,
			     std::vector<std::vector<double> > &v);
	Eigen::MatrixXd convertToMatrix(std::vector<std::vector<double> > &data);
	Eigen::MatrixXd rotateData(dataset *dt, Eigen::MatrixXd& M);
	Eigen::MatrixXd convertDfToMatrix(const dataset* data,
					std::vector<int> &sampleIndex);
	std::vector<double> pathLength(std::vector<double> &inst);
	double getdepth(std::vector<double> &inst, Tree* tree,Eigen::MatrixXd &rotmat,double* transInst);
	void rForest();
	int adaptiveForest(double alpha,int stopLimit); 
    void fixedTreeForest();
    void projectedForest();
};
#endif /* RFOREST_H_ */

