#include "metric.hpp"
using namespace std;
namespace metric {

double add(double a, double b){
  return a+b;
}
/* Caculate the trapezoidal area bound by the quad (X1,X2,Y1,Y2)*/
double trapezoidArea(double X1, double X2, double Y1, double Y2) {
  double base   = std::abs(X1-X2);
  double height =     (Y1+Y2)/2.0;
  return (base * height);
}

double AUC(vector<double> &labels, vector<double> &scores,int n,int posclass) {
  typedef std::pair<float,int> mypair;
  std::vector<mypair> L(n);
  for(int i = 0; i < n; i++) {
    L[i].first  = scores[i];
    L[i].second = labels[i];
  }
  std::sort   (L.begin(),L.end());
  std::reverse(L.begin(),L.end());

  /* Count number of positive and negative examples first */
  int N=0,P=0;
  for(int i = 0; i < n ; i++) {
    if(labels[i] == posclass) P++;
    else N++;
  }
  if( N == 0 || P == 0 )
    std::cout<<"I only found class 1 in the labels vector ...\n";

  /* Then calculate the actual are under the ROC curve */
  double              A       = 0;
  double              fprev   = -99999;//INT_MIN; //-infinity
  unsigned long long	FP      = 0,
      TP      = 0,
      FPprev  = 0,
      TPprev  = 0;

  for(int i = 0 ; i < n; i++) {
    double fi   = L[i].first;
    double label= L[i].second;
    if(fi != fprev) {
      /* Divide area here already : a bit slower, but gains in precision and avoids overflows */
      A       = A + (trapezoidArea(FP*1.0/N,FPprev*1.0/N,TP*1.0/P,TPprev*1.0/P));
      fprev	= fi;
      FPprev	= FP;
      TPprev	= TP;
    }
    if(label  == posclass)
      TP = TP + 1;
    else
      FP = FP + 1;
  }
  /* Not the same as Fawcett's original pseudocode though I think his contains a typo */
  A = A + trapezoidArea(1.0,FPprev*1.0/N,1.0,TPprev*1.0/P);
  return A;
}





}
