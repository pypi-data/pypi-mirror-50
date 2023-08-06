/*
 * test_FacadeForest.cpp
 *
 *  Created on: May 4, 2016
 *      Author: tadeze
 */


#include "facade_forest.hpp"
#include "gtest/gtest.h"
#include "common_util.hpp"
class FacadeForestTest : public ::testing::Test
{
protected:
	 FacadeForest ff;
	 std::vector<std::vector<double> > data ;
	 const int DIM=4;
	 const int NROW = 1000;
	 const int NTREE = 100;
	 const int nsample = 256;
	 //util::dataset *dataset;
     virtual void SetUp() {

    	 //Let read data from
         //std::string filename = common::filename();
    	 //data= util::readcsv((char*) &filename[0],',',true);
		std::vector<std::vector<double> > dataxx = util::syntheticData(DIM, NROW);

    	 int tree_used = ff.trainForest(dataxx, NTREE,nsample,0,false,false,false,0.01,0);  //Just train a forest
	   	 ff.testForest(data,false);
     }

     virtual void TearDown()
     {
    	// delete ff;
     }
};

//
//TEST_F(FacadeForestTest, creatFF){
//
////	ASSERT_EQ(ff.getNSample(),nsample);
////	ASSERT_EQ(ff.getNTree(),NTREE);
////	ASSERT_EQ(ff.getTraindf()->nrow,NROW);
//ASSERT_FALSE(false);

//}


TEST_F(FacadeForestTest, createScore){

	std::vector<double> scores = ff.getScore();
	 std::sort(scores.begin(),scores.end());
	 EXPECT_GT(scores[104],0.5852);
	 EXPECT_LT(scores[0],0.453423);
	 EXPECT_GT(scores[50],0.450967);

}
TEST_F(FacadeForestTest, pathLength){

	std::vector<std::vector<double> > depths = ff.pathLength();
	EXPECT_EQ(depths.size(),NROW);  //Make sure dimension first
	EXPECT_EQ(depths[0].size(),NTREE);
	 auto scores = ff.getScore();
	 std::sort(scores.begin(),scores.end());
	 EXPECT_GT(scores[104],0.74852);
	 EXPECT_LT(scores[0],0.453423);
	 EXPECT_GT(scores[50],0.450967);

}
TEST_F(FacadeForestTest, avgDepth){
	std::vector<double> scores = ff.averageDepth(); //average depth
	 std::sort(scores.begin(),scores.end());
	 EXPECT_GT(scores[104],3);
	 EXPECT_LT(scores[0],10);
	 EXPECT_GT(scores[50],7);

}
#ifdef SERIALIZATION

TEST_F(FacadeForestTest, saveModel){
    ff.save("qtrial.cereal");
    std::ifstream in("qtrial.cereal");
    //check if the file is not empty
    ASSERT_FALSE(in.peek()==std::ifstream::traits_type::eof());
}


TEST_F(FacadeForestTest, LoadModel){
    FacadeForest facaf;
    facaf.load("qtrial.cereal");
	ASSERT_EQ(facaf.getNTree(),100);
   //ASSERT_EQ(facaf.getIff()->ntree,100);
   //Empty file 
   /*facaf = new FacadeForest();
   facaf.load("empty.json",FacadeForest::FOREST::IFOREST);
   ASSERT_NULL(facaf.getIff());
*/
}
#endif

TEST_F(FacadeForestTest,adaptiveTrain){
	FacadeForest adaptForest;

	int ntree = adaptForest.trainForest(data,100,256,0,false,true,false,0.01,0);  //Just train a forest
	ASSERT_EQ(100,ntree);


}

