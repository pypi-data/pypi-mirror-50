#include "metric.hpp"
#include <gtest/gtest.h>
// Tests positive input.


TEST(IsAUCTest, Positive) {
 std:: vector<double> lbl ={1,0,1,1};
 std::vector<double> score = { 0.34,0.52,0.26,0.84};
 double auc = metric::AUC(lbl,score,4,1);
 EXPECT_EQ(auc,(double)1/3);

  
  
}

TEST(IsAUCTest,oneAUC ) {
 std:: vector<double> lbl ={1,1,1,0,0,0,0};
  std::vector<double> score = { 0.84,0.5,0.6,0.2,0.05,0.08,0.17};
  double auc = metric::AUC(lbl,score,7,1);
  EXPECT_EQ(auc,1);
}

TEST(IsAUCTest,ZeroAUC ) {
 std:: vector<double> lbl ={1,1,1,0,0,0,0};
  std::vector<double> score = { 0.84,0.5,0.6,0.2,0.05,0.08,0.17};
  double auc = metric::AUC(lbl,score,7,0);
  EXPECT_EQ(auc,0);
}

TEST(IsAUCTest,HalfAUC ) {
 std:: vector<double> lbl ={1,1,1,1,0,0,0,0,0,0};
 std::vector<double> score = { 0,0,0,0,0,0,0,0,0,0};
 double auc = metric::AUC(lbl,score,10,1);
 EXPECT_EQ(auc,0.5);
}



/*
int main(int argc, char ** argv)
{
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}



int main()
{
    std:: vector<double> lbl ={1,1,0,1,0,0,0};
    std::vector<double> score = { 0.34,0.5,0.6,0.2,0.5,0.8,0.7};
    double auc = metric::AUC(lbl,score,7,1);
    std::cout<<metric::INT_MAX<<"test starting "<<auc<<std::endl;
    return 0;
}

*/

