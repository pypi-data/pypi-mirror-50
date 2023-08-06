/*
 * main.cpp
 *
 @Created on: Mar 22, 2015
 * @Author: Tadeze
 * Main entry: accepts the the
 * @param argv
 *    Usage: iforest [options]
 *      -i FILE, --infile=FILE
 Specify path to input data file. (Required).
 -o FILE, --outfile=FILE
 Specify path to output results file. (Required).
 -m COLS, --metacol=COLS
 Specify columns to preserve as meta-data. (Separated by ',' Use '-' to specify ranges).
 -t N, --ntrees=N
 Specify number of trees_ to build.
Default value is 100.
 -s S, --sampsize=S
 Specify subsampling rate for each tree. (Value of 0 indicates to use entire data set).
 Default value is 2048.
 -d MAX, --maxdepth=MAX
 Specify maximum depth_ of trees_. (Value of 0 indicates no maximum).
 Default value is 0.
 -H, --header
 Toggle whether or not to expect a header input.
 Default value is true.
 -v, --verbose
 Toggle verbose ouput.
 Default value is false.
 -h, --help
 Print this help message and exit.
 */

#include "facade_forest.hpp"
#include "command_parser.hpp"
#include "bagged_forest.hpp"

//log file
#include <cmath>
/*
 * Display vector data
 */



std::ofstream osu::ad::util::log_file; //("log_file.csv");

inline std::vector<int> fill_vector(int start, int end, int step = 1){
    std::vector<int> data;
    for(int i=start; i<end;i+=step) data.push_back(i);
    return data;
}
inline std::shared_ptr<osu::ad::util::Dataset> make_dataset(std::vector<std::vector<double> > &data) {
    std::shared_ptr<osu::ad::util::Dataset> dt = std::make_shared<osu::ad::util::Dataset>();
    dt->data = data;
    dt->ncol = (int) data[0].size();
    dt->nrow = (int) data.size();
    return dt;
}

void testBaggedForest(){
    std::cout<<" Checking Bagged forest \n";
    std::vector<std::vector<double> > dataxx = osu::ad::util::synthetic_data(4, 1000);   //util::readcsv((char *) &filename[0], ',', true);

    //util::write_log(filename);
    //util::close_log();
    bool check_missing_value = true;//false;//true;

    auto dataset = make_dataset(dataxx);
    // From facadeForest
  osu::ad::BaggedForest bf(100, dataset, 256, 0 , false, true);
    bf.check_missing_value_ = true;
    bf.buidForest();
    std::cout<< bf.instance_score(dataxx[0]);
    std::cout<<"\n End of bagged forest \n";
}

int main(int argc, char** argv) {
 Parser args;
    args.parse_argument(argc, argv);
    args.display_argument();

   // util::debug = seed;
    //util::initialize();
    std::string input_name = args.input_name;
    std::string output_name = args.output_name;
    std::string test_name = args.test_name;
    std::string load_forest = args.loadpath;
    std::string save_forest = args.savepath;
    std::string meta_cols = args.metacols;
    int ntree = args.ntrees;
    int nsample = args.nsample;
    int maxheight = args.maxdepth;
    bool header = args.header;

  /*  bool use_subsample_ = num_sample_ != 0;
    bool stop_height_ = max_height_ != 0;
    int stop_limit_ = pargs->adaptive_;
    bool rangecheck = pargs->rangecheck;
    bool rotate_ = pargs->rotate_;
    bool pathlength = pargs->pathlength;
    float rho_ = pargs->precision;
    float alpha = pargs->alpha;
    int epoch = pargs->epoch;
    bool oob = pargs->oobag;

    //Input file to dataframe_
    bool explanation = pargs->explanation;

*/
}

void experimentalCodes(){
    //parseInput(argc,argv);
    //Tree::range_check = true;
  osu::ad::util::log_file.open("log_file.txt",std::ios_base::out);
    //std::string log_filename ("outputlog.txt");
    //util::init_log(log_filename);

    //Parser args;

    //args.parse_argument(argc, argv);

    /*std::string filename = args.input_name;//util::filename();
    int num_trees_ = args.ntrees;
    int num_sample_ = args.num_sample_;
    */
    // TODO: Incorporate the command parser into main file


    std::vector<std::vector<double> > dataxx = osu::ad::util::synthetic_data(4, 1000);   //util::readcsv((char *) &filename[0], ',', true);
    testBaggedForest();



    //util::write_log(filename);
    //util::close_log();
    bool check_missing_value = true;//false;//true;

    // From facadeForest
  osu::ad::FacadeForest ff;
    std::vector<int> columnindx = {}; //0,1,2};
  ff.train(dataxx, 100, 256, 0, false, false, false, 0.01, 0, columnindx);
    std::cout << ff.num_sample() << " ==" << ff.num_trees() << std::endl;
    std::cout <<"Size of training set"
              <<dataxx.size()
              <<","<<dataxx[0].size()<<std::endl;
    // Insert missing values.

    auto dataset = make_dataset(dataxx);
    auto indexx = fill_vector(0, 256, 1);
    auto tree = std::make_shared<osu::ad::Tree>(); //Tree();
    tree->iTree(indexx,dataset,0, 0, false);
    std::cout<< tree->path_length(dataset->data[0], true)<<"\t";
    std::cout<<dataset->data[0][0];
    dataset->data[0][0] = NAN;
    std::cout<<dataset->data[0][0];
//    dataxx[0][0] = NAN;// -9999.0;
//    dataxx[0][1] = NAN;
//    dataxx[3][1] = NAN;
//    dataxx[4][1] = NAN;
//    dataxx[4][2] = NAN;

  ff.score(dataxx, check_missing_value);
    std::vector<double> score = ff.anomaly_score();

    std::cout<<"Checking scores\n";
//    for (auto const &sce : score)
//        std::cout << sce << "\t";
    std::cout<<"\n checking path"<<std::endl;

    std::cout<< tree->path_length(dataset->data[0], true)<<"\t";
    std::cout<< tree->path_length(dataset->data[0], false);





    //std::string forest_name = "facadeforest.bin";
//    std::ofstream tracedpath("tracedpath2.csv");
//    ff.explanation(dataxx[2]);
//    ff.trace_path(dataxx[2],tracedpath);
//    tracedpath.close();

    //ff.save(forest_name,true);


    /** checking from forest **/

//    std::shared_ptr<util::Dataset> Dataset;
//    Dataset = data::make_dataset(data);
//
//    std::cout<<Dataset->data[5][0]<<"\n";
//    int i = 2;
//    std::cout << Dataset->ncol << " Column \n";
//    Dataset->print(i);
//    auto explan = ff.explanation(Dataset->data[i]);
//    std::cout << "\n Explanations" << std::endl;
//    for (const auto &mpr : explan)
//        std::cout << mpr.first << "\t" << mpr.second << std::endl;


    // Register the derivedtype class
    // Serialize
/*
    std::string filenamex{"forest.cereal"};
    {
    std::ofstream file{filenamex};
    if (!file.is_open()) {
        throw std::runtime_error{filenamex + " could not be opened"};
    }
    //cereal::JSONOutputArchive archive{file};
    cereal::BinaryOutputArchive archive{file};
    archive(ff);
    }
*/
    // Read forest

    /*      std::ifstream ifile{filenamex};
          if (!ifile.is_open()) {
              throw std::runtime_error{filenamex + " could not be opened"};
          }
          FacadeForest newff;
         //cereal::JSONInputArchive iarchive{ifile};
         cereal::BinaryInputArchive iarchive(ifile); // Create an input archive
          iarchive(newff);

          newff.score(data,check_missing_value);
          auto  new_score = newff.anomaly_score();
         for(auto &sc : new_score)
             std::cout<<sc<<"\t";
  */
    // TODO: explanation returns vad pointer need to be updated.
    // auto tr = std::make_shared<Tree>();
    //tree_sh->iTree(dataIndex,Dataset,0,0,false)


    /* checking contributions  from trees_ **/
    //std::vector<std::vector<double> > data = util::readcsv((char*) &filename[0],',',true);

//	Tree *tr = new Tree();
    /*
    std::vector<int> dataIndex;//(Dataset->nrow);
    for(int i=0;i<Dataset->nrow;i++)
        dataIndex.push_back(i);
    tr->iTree(dataIndex,Dataset,0,0,false);
    std::cout<<tr->path_length(Dataset->data[4])<<" Depth\n";
    std::cout<<"Feature explanations\n";

    auto feature = tr->explanation(Dataset->data[5]);
   */
    // archive(cereal::make_nvp("tree",tr));
    //file.close();

/*	std::cout<<feature.size()<<std::endl;
	//Dataset->print(2
  for(const auto & mpr : feature)
		std::cout<<mpr.first<<"\t"<<mpr.second<<std::endl;
*///
    //  std::cout<<" Second anomalies";
//    feature = tr->feature_contribution(Dataset->data[4]);
//    std::cout<<feature.contributions.size()<<std::endl;
//    Dataset->print(4);
//    for(const auto & mpr : feature.feature_contribution())
//        std::cout<<mpr.first<<"\t"<<mpr.second<<std::endl;


    /*for(auto sc : score){
           std::cout<<sc<<std::endl;

       }
    */
    //display_vec(ff.getTraindf()->data);

    /* util::Dataset *dt = make_dataset(data);

     std::cout<<dt->nrow<<","<<dt->ncol<<" Row/column"<<std::endl;

     IsolationForest forest_(100,dt,256,0,false,false);
     forest_.fixed_forest();
     std::vector<double> score = forest_.anomaly_score(dt);
     for(auto sc : score){
         std::cout<<sc<<std::endl;

     }
     delete dt;
 */
    //util::log_file.close();
}


//TODO: Change the data datastructure to using Eigen or custom Matrix.








