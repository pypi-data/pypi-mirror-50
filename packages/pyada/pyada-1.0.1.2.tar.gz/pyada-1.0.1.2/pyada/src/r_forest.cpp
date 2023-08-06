//TODO: Random rotation with reduced dimension of ceil(sqrt(d)/2) +2
//TODO: Remove the doubleframe and replace with dataset array.
#include "r_forest.hpp"
/*
 * Class for RandomRotation Matrix
 *
 */
using namespace Eigen;

/*Take Matrix and return doubleframe
 */
void  RForest::convertToDf(MatrixXd &m,dataset* df)
{

   
    for (int i=0; i<m.rows(); ++i)
    {
     	df->data[i] = &m.row(i).data()[0];//copy to dataframe   
    }
}

/* Rotate data instance with rotation matrix
 */
void RForest::rotateInstance(std::vector<double> &inst,MatrixXd &m,double* rotData)
{

	int ncol = m.cols();
	MatrixXd matData = Map<MatrixXd>(inst,1,ncol);
	MatrixXd rotMat = matData*m;
	Map<MatrixXd>(rotData,rotMat.rows(),rotMat.cols()) = rotMat;

}


/*
 * Takes matrix and empty vector data
 * Fill the vector-2d with the matrix value
 */
void RForest::convertToVector(MatrixXd &m, std::vector<std::vector<double> > &v)
{
    for (int i=0; i<m.rows(); ++i)
    {
        const double* begin = &m.row(i).data()[0];
        v.push_back(std::vector<double>(begin, begin+m.cols()));
    }
}

/*
 * Takes dataset of vector<vector<double> > and return Matrix of data
 */
MatrixXd RForest::convertToMatrix(std::vector<std::vector<double> > &data) 
{
	MatrixXd mat(data.size(), data[0].size());
	for (int i = 0; i <(int)data.size(); i++)
	      mat.row(i) =VectorXd::Map(&data[i][0],(int)data[i].size());
	return mat;
}

/* 
 * Convert doubleframe data to Matrix
 *
 */
/*
MatrixXd RForest::convertDfToMatrix(const doubleframe* data,
        std::vector<int> &sampleIndex)
{
	MatrixXd mat((int)sampleIndex.size(), data->ncol);
	for (int i = 0; i <(int)sampleIndex.size(); i++)
	  mat.row(i) =VectorXd::Map(&data->data[sampleIndex[i]][0],data->ncol);
	return mat;
}*/

/*
 * Rotation matrix generator reference paper:
 * @input Matrix empty matrix
 * @input n size of matrix //will remove later and seed as well need to remove it
 */
 void RForest::generateRandomRotationMatrix(MatrixXd& M,int n)
{

   	std::normal_distribution<double> distribution(0.0, 1.0);
	MatrixXd A(n, n);
	const VectorXd ones(VectorXd::Ones(n));
	for (int i = 0; i<n; i++)
	{
		for (int j = 0; j<n; j++)
		{
			A(i, j) = distribution(this->eng); //generator);  //mtrand.randNorm(0, 1);

		}
	}
	const HouseholderQR<MatrixXd> qr(A);
	const MatrixXd Q = qr.householderQ();
	M = Q*(qr.matrixQR().diagonal().array() <0).select(-ones, ones).asDiagonal();
	if (M.determinant()<0)
	for (int i = 0; i<n; i++)
		M(i, 0) = -M(i, 0);

}

/*
* Rotate a give datafram data
* @input dt  doubleframe data
* @input M Rotation matrix
* @return rotated Matrix data
*/

MatrixXd  RForest::rotateData(dataset* dt, MatrixXd& M)
{ 
    std::vector<int> sampleIndex(this->nsample);
	getSample(sampleIndex,nsample,rsample,dt->nrow);
    MatrixXd  mData = convertDfToMatrix(dt,sampleIndex);
    return mData*M;
}
void RForest::fixedTreeForest()
{
    rForest();
}

/*
 * Build rotation forest by rotating with random rotation matrices
 */
void RForest::rForest()
{
    //Build the RForest model 
    std::vector<int> sampleIndex(this->nsample);
    doubleframe* sampleDf = new doubleframe();
    sampleDf->data = new double*[this->nsample];
    //logfile<<"point,tree,x1,x2\n";

    for(int n=0;n<ntree;n++)
          {
            //get sample data
            getSample(sampleIndex,nsample,rsample,dataset->nrow);
            
            MatrixXd rotMat(dataset->ncol,dataset->ncol);
            generateRandomRotationMatrix(rotMat,dataset->ncol);
            
            //Save rotation matrix
            this->rotMatrices.push_back(rotMat);

            //Rotate data and convert to doubleframe format
            MatrixXd rotData =convertDfToMatrix(dataset,sampleIndex)*rotMat;
            sampleDf->nrow = this->nsample;
            sampleDf->ncol = rotMat.cols();
            convertToDf(rotData,sampleDf);
            
            //Fill the sampleIndex with indices of the sample rotated data
            sampleIndex.clear();

            for(int i=0;i<sampleDf->nrow;i++) sampleIndex.push_back(i);
            Tree *tree  = new Tree();

            tree->iTree(sampleIndex,sampleDf,0,maxheight,stopheight);
            this->trees.push_back(tree);

            }
    delete[] sampleDf->data;
    delete sampleDf;
}


/*
 * Build Trees in adaptive ways
 */

int RForest::adaptiveForest(double alpha,int stopLimit){
    //Build the RForest model
    double tk = ceil(alpha*2*dataset->nrow);
    std::vector<int> sampleIndex(this->nsample);
    doubleframe* sampleDf = new doubleframe();
    sampleDf->data = new double*[this->nsample];
    //logfile<<"point,tree,x1,x2\n";
    bool converged = false;
    int convCounter =0 ;
    double ntree=0;
    std::vector<int> topKIndex;
    std::vector<int> prevTopKIndex;
    std::vector<double> totalDepth(dataset->nrow,0);
    double prob=0.0;
    std::priority_queue<std::pair<int,double>,std::vector<std::pair<int,double> >, larger> pq;
    double* transInst = new double[dataset->ncol];
   //util::logfile<<"0,0,0,0,0,0,0,0,0\n";
    while(!converged)
    {
    	pq= std::priority_queue<std::pair<int,double>,std::vector<std::pair<int,double> >,larger >();

            //get sample data
            getSample(sampleIndex,nsample,rsample,dataset->nrow);

            MatrixXd rotMat(dataset->ncol,dataset->ncol);
            generateRandomRotationMatrix(rotMat,dataset->ncol);
            //Save rotation matrix
            this->rotMatrices.push_back(rotMat);
            //Rotate data and convert to doubleframe format
            MatrixXd rotData =convertDfToMatrix(dataset,sampleIndex)*rotMat;
            sampleDf->nrow = this->nsample;
            sampleDf->ncol = rotMat.cols();
            convertToDf(rotData,sampleDf);

            //Fill the sampleIndex with indices of the sample rotated data
            sampleIndex.clear();
            for(int i=0;i<sampleDf->nrow;i++) sampleIndex.push_back(i);

            Tree *tree  = new Tree();
            tree->iTree(sampleIndex,sampleDf,0,maxheight,stopheight);
            this->trees.push_back(tree);
            ntree++;
            double d,dbar;
            topKIndex.clear();
            for (int inst = 0; inst <dataset->nrow; inst++)
            {
            d = getdepth(dataset->data[inst],tree,rotMat,transInst);
            totalDepth[inst] += d;
            dbar=totalDepth[inst]/ntree;
            pq.push(std::pair<int, double>(inst,dbar));
           	}
      //      util::logfile<<ntree<<",";
        for(int i=0;i<tk;i++)
         {
        	  	topKIndex.push_back(pq.top().first);
        	//  	util::logfile<<pq.top().first<<",";
        	  	pq.pop();

        }

        if(ntree==1)
        {
        	prevTopKIndex = topKIndex;
        //	util::logfile<<prob<<"\n";
           	continue;
        }

        prob=topcommonK(topKIndex,prevTopKIndex);
        prevTopKIndex = topKIndex;
       // util::logfile<<prob<<"\n";
        if(prob==1)
             convCounter++;
          else
            convCounter=0;
         converged = convCounter>stopLimit;


         if(ntree<50)
             	  converged=false;



    }




delete transInst;
delete[] sampleDf->data;
delete sampleDf;
return ntree;
}



/*
 * overrides method of pathLength for rotated data
 */
std::vector<double> RForest::pathLength(double *inst)
{
    std::vector<double> depth;
    int i=0;
    double* transInst=new double[dataset->ncol];//NULL;
    
   for(std::vector<Tree*>::iterator it=this->trees.begin();it!=trees.end();it++)
    {   
    	depth.push_back(getdepth(inst,*it,this->rotMatrices[i],transInst));
        i++;
     }

delete transInst;
return depth;
}

double RForest::getdepth(double* inst, Tree* tree, MatrixXd &rotmat,double* transInst)
{

	rotateInstance(inst,rotmat,transInst);
	return tree->pathLength(transInst);

}

/*
 * Build rotation forest by rotating with reduced dimension of \sqrt(d)/2 +2
 */
void RForest::projectedForest()
{
    //Build the RForest model 
    std::vector<int> sampleIndex(this->nsample);
    doubleframe* sampleDf = new doubleframe();
    sampleDf->data = new double*[this->nsample];
    //logfile<<"point,tree,x1,x2\n";
    int rfeatures = ceil(sqrt(sampleDf->ncol)/2)+2;
    for(int n=0;n<ntree;n++)
          {
            //get sample data
            getSample(sampleIndex,nsample,rsample,dataset->nrow);
            
            MatrixXd rotMat(rfeatures,rfeatures);
            
            generateRandomRotationMatrix(rotMat,dataset->ncol);
          
            //Save rotation matrix
            this->rotMatrices.push_back(rotMat);

            //Rotate data and convert to doubleframe format
            MatrixXd rotData =convertDfToMatrix(dataset,sampleIndex)*rotMat;
            sampleDf->nrow = this->nsample;
            sampleDf->ncol = rotMat.cols();
            convertToDf(rotData,sampleDf);
            
            //Fill the sampleIndex with indices of the sample rotated data
            sampleIndex.clear();

            for(int i=0;i<sampleDf->nrow;i++) sampleIndex.push_back(i);
            Tree *tree  = new Tree();

            tree->iTree(sampleIndex,sampleDf,0,maxheight,stopheight);
            this->trees.push_back(tree);

            }
    delete[] sampleDf->data;
    delete sampleDf;
}


