//
// Created by tadeze on 9/15/17.
//
#include "include/parser/parser.hh"
#include "command_parser.hpp"
#include<fstream>

/*
 * /*Options:
	-i FILE, --infile=FILE
		Specify path to input data file. (Required).
	-o FILE, --outfile=FILE
		Specify path to output results file. (Required).
	-m COLS, --metacol=COLS
		Specify columns to preserve as meta-data. (Separated by ',' Use '-' to specify ranges).
	-t N, --ntrees=N
		Specify number of trees_ to build.(Value 0 indicates to use adaptive_ tree growing)
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
		Toggle verbose output.
		Default value is false.
	-a (null), --adaptive_=(null)
		Number of common successive top K for adaptive_ process.
		Default value is 5.
	-r, --rotate_
		Toggle whether to rotate_ data or not.
		Default value is false.
	-c N, --columns=N
		specify number of columns to use.
		Default value is 0.
	-p, --pathlength
		Toggle whether to display  depth_ of all trees_ (Default is false)
		Default value is false.
	-x FILE, --testfile=FILE
		Specify path to test file. (optional).
	-g, --rangecheck
		Toggle whether to use range check or not during testing (Default false)
		Default value is false.
	-j P, --precision=P
		Specify rho_ precision confidence interval for stopping criteria Value (0.01 to 0.08) works
		Default value is -3.0.
	-q Q, --alpha=Q
		Anomaly proportion. Default 0.01
		Default value is 0.01.
	-e E, --epoch=E
		Specify number of epoch when batch mode training is selected. Default 30
		Default value is 0.
	-z seed, --seed=seed
		Specify seed for randomization. Default random seed
		Default value is -1.
	-l, --explain
		Toggle whether to output feature explanation or not.
		Default value is false.
	-k, --oob
		Check if you want use out of bag estimate for scoring. Default false.
		Default value is false.
	-b FILE, --save=FILE
		Specify path to save iforest model.
	-f FILE, --load=FILE
		Specify path to load saved iforest model, if you want to load from saved forest.
	-h, --help
		Print this help message and exit.
 *
 *
 */
bool checkExist(std::string fileName){
    std::ifstream infile(fileName.c_str());
    if(!infile.good())
        throw std::runtime_error{fileName+" could not be opened"};
    return true;
}
void Parser::display_argument() {
std::cout<<"Num trees_: "<<ntrees;
}
void Parser::parse_argument(int argc, char **argv) {


    optionparser::parser p("IsolationForest commandline options ");

    p.add_option("--num_trees_", "-t")
            .help("Number of trees_.")
            .required(true)
            .mode(optionparser::store_value)
            .default_value(100);
    p.add_option("--num_sample_","-s").help("Sample size. Default 512.")
            .mode(optionparser::store_value)
            .required(false)
            .default_value(512);
    p.add_option("--input","-i")
            .help("Input csv file required.")
            .required(true)
            .mode(optionparser::store_value);
    p.add_option("--output","-o")
            .help("Output csv file required")
            .required(true)
            .mode(optionparser::store_value);

    p.add_option("--metacols","-m")
            .help("Metacolumn to skip. ")
            .mode(optionparser::store_mult_values);
    p.add_option("--max_height_", "-d")
             .help("Max depth_ for the tree to grow. Defualt 0 (grow until separation)")
             .default_value(0)
            .mode(optionparser::store_value);
    p.add_option("--pathlength","-p")
            .help("Toggle whether to display depth_ of all trees_ or not. Default false")
            .mode(optionparser::store_true).default_value(false);
    p.add_option("--testfile", "-x")
            .help("Specify path to test file. (optional)")
            .mode(optionparser::store_value);
    p.add_option("--explain","-l")
            .help("Toggle whether to output feature explanation")
            .default_value(false).mode(optionparser::store_true);
    p.add_option("--save","-b")
            .help("Specify  file name to save the trianed model")
            .mode(optionparser::store_value);
    p.add_option("--load","-f")
            .help("Specify  file name to load the trianed model")
            .mode(optionparser::store_value);
    p.add_option("--missvalue","-j")
            .help("Specify missing vlaue. Defualt false.")
            .default_value(false)
            .mode(optionparser::store_true);

    p.eat_arguments(argc, argv);


// Assign and validate values.
    if (p.get_value("input")) {
        input_name = p.get_value<std::string>("input");
        //input_name = names;
        checkExist(input_name);
    }
    if(p.get_value("num_sample_")) {
        nsample = p.get_value<int>("num_sample_");
    }

    if(p.get_value("num_trees_")) {
        ntrees = p.get_value<int>("num_trees_");
        if (ntrees==0)
            adaptive=true;
    }

    if(p.get_value("output")) {
        output_name = p.get_value<std::string>("output");
    }
    if(p.get_value("max_height_"))
        maxdepth = p.get_value<int>("max_height_");
    if(p.get_value("pathlength"))
        pathlength = p.get_value<bool>("pathlength");
    if(p.get_value("testfile")) {
        test_name = p.get_value<std::string>("testfile");
        checkExist(test_name);
    }
    if(p.get_value("explain"))
        explain = p.get_value<bool>("explain");
    if(p.get_value("save"))
        savepath = p.get_value<bool>("save");
    if(p.get_value("load")) {

        loadpath = p.get_value<bool>("load");
        checkExist(loadpath);
    }

    if (p.get_value("metacols")) {
        metacols = p.get_value<std::string>("metacols");
        //gComponent = names;
    }
    if(p.get_value("missvalue"))
        range_check = p.get_value<bool>("missvalue");


}