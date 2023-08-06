//
// Created by tadeze on 5/7/17.
//

#ifndef PYIFOREST_IOPARSER_HPP
#define PYIFOREST_IOPARSER_HPP

#include <vector>
#include <ostream>

namespace osu {
namespace data {
    class IOParser {

    };
   /* class Dataset{

    };*/
    struct dataset
    {
        int ncol;
        int nrow;
        std::vector<std::vector<double> > data;
        //std::vector<std::vector<double> > data;
        void print(int ix,std::ostream &out){
            for(auto elem : data[ix])
                out<<elem<<"\t";
        }
    };
}

}
#endif //PYIFOREST_IOPARSER_HPP
