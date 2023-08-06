/*
 * test_Forest.cpp
 *
 *  Created on: May 4, 2016
 *      Author: tadeze
 */



#include "forest.hpp"
#include "gtest/gtest.h"
#include "isolation_forest.hpp"
#include "common_util.hpp"
class ForestTest : public ::testing::Test {
protected:
	std::shared_ptr<Forest> ff;
	std::vector<std::vector<double> > data ;
	std::shared_ptr<util::dataset> dataset;
	 int ntree,nsample,maxheight;
	 bool rsample,stopheight;
	int DIM = 4;
	int NROW = 1000;
	virtual void SetUp() {
    	ntree=100;
    	nsample=50;
    	maxheight=0;
    	rsample=false;
    	stopheight=false;
    	 //Forest(int _ntree,util::dataset* _dataset,int _nsample,int _maxheight, bool _stopheight,bool _rsample)

    	 //Let read data from
    	 //std::string filename("./synth2d.dt");
        // std::string filename = common::filename();
    	// data= util::readcsv((char*) &filename[0],',',true);
    	 //ff = new FacadeForest();
		  std::vector<std::vector<double> > data = util::syntheticData(DIM, NROW);
    	  dataset = common::makeDataset(data);
    	  ff = std::make_shared<IsolationForest>(ntree,dataset,nsample,maxheight,stopheight,rsample);

     }

     virtual void TearDown()
     {
    	//delete dataset;
    	//delete ff;
     }
};


TEST_F(ForestTest, createForest){
    ff->fixedTreeForest();
    ASSERT_EQ(ff->nsample,nsample);
	ASSERT_EQ(ff->ntree,ntree);
	ASSERT_FALSE(ff->rsample);
	ASSERT_EQ(ff->maxheight,maxheight);

}

/*
TEST_F(ForestTest,serialize)
{
   // ASSERT_EQ(9,9);
    // Test serialization of the Forest.
    ff->fixedTreeForest();
    json jj =  ff->to_json();
   ASSERT_EQ(jj["ntree"],ff->ntree);
   ASSERT_EQ(jj["nsample"],ff->nsample);

   std::ofstream ll("forest.json");
   ll<<jj;
   ll.close();

}

TEST_F(ForestTest,deserialize){
   Forest* forest;
   IsolationForest iff;
    forest = &iff;
    std::ifstream in("forest.json");
    //json jj;
    //in>>jj;
    forest->from_json(in);
   ASSERT_EQ(forest->ntree,ntree);
   ASSERT_EQ(forest->nsample,nsample);
    //just take two random node and check they are equal

}*/
//Test remaining module in child

