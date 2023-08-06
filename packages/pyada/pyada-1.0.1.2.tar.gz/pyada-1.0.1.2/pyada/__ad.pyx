"""
@Author: Tadesse Zemicheal

"""
#__all__ = ['IsolationForest','IsolationTree', 'IForest', 'RotationForest']

from collections import defaultdict
cimport numpy as np
import numpy as np
import pickle
from .ad cimport *
#NA = -9999.0




cdef class IsolationForest:
    
    cdef FacadeForest * thisptr
    cdef int ntree, nsample, maxheight, stoplimit
    cdef float rho
    cdef bool rotate, adaptive, rangecheck
    # cdef bool is_trained = False

    def __cinit__(self, x=None, ntree=100, nsample=512, maxheight=0,
                  rotate=False, adaptive=False, rangecheck=True, rho=0.01, stoplimit=5):
        """
        Create IsolationForest object. If parameters are given, the forest is trained using train() method, otherwise empty
        object is created to be trained later.

        Args:
            x: (ndarray) Training dataset of ndarray(numpy matrix) format. Required field
            ntree: (int) Number of trees used. Default 100
            nsample: (int) Number of subsample size for training. Defualt 512. If nsample = 0 all training data is used. 
            maxheight: (int) Maximum depth of the binary trees. Default 0 means grow tree until full isolation.
            rotate: (bool) Toggle for rotating forest or not. Default false.
            adaptive: (bool) Toggle for using adaptive method of growing trees. Default false.
            rangecheck: (bool) Toggle for rangecheck during scoring points. Default true.
            rho: (float) Specify rho precision confidence interval for stopping criteria Value (0.01 to 0.08) works. 
                 Default value 0.01. Used only if adaptive is True.
            stoplimit: (bool) Number of common successive top K for adaptive process. Default 5.Used only if adaptiv is True
        E.g.
        >> ff = IsolationForest(x=train_data, ntree=100, nsample=100)
        >> ff.score(x=test_data)
        
        Returns: IsolationForest object. 
        """
        #self.is_trained = False
        self.thisptr = new FacadeForest()
        self.ntree = ntree
        self.nsample = nsample
        self.maxheight = maxheight
        self.rotate = rotate
        self.adaptive = adaptive
        self.rangecheck = rangecheck
        self.rho = rho
        self.stoplimit = stoplimit
        if x is not None:
            self.train(x)

    def __dealloc__(self):
        del self.thisptr

    def train(self, x, column_subsample=[]):
        """
        Train Isolation Forest model.
        ff.train_forest(_traindf,_ntree=100,_nsample=512,_maxheight=0,_rotate=False,_adaptive=False,_rangecheck=True,_rho=0.01,_stoplimit=5,
        column_subsample=[]):

        Args:
            x: Training dataset of ndarray(numpy matrix) format. Required field
            column_subsample: if specified it uses only column specified. 
        Returns: Trained IsolationForest object 
        """

        DataValidator.validate_dataset(x)
        if self.ntree < 0:
            raise NameError("Number of trees cann't be less than 0")
        if self.ntree == 0:
            print ("You set 0 number of trees, then it is adaptive way of growing")
            adaptive = True
        if self.nsample > len(x) or self.nsample == 0:
            self.nsample = len(x)
            print(
                "Number of samples cann't be greater than sample size,then data will be used")
        if self.maxheight < 0:
            raise NameError("Max depth cann't be negative")
        if self.rho > 1:
            raise NameError("rho value should be less than 1")
        #self.is_trained = True

        return self.thisptr.train(x, self.ntree, self.nsample, self.maxheight,
                                        self.rotate, self.adaptive, self.rangecheck, self.rho,
                                        self.stoplimit, column_subsample)


    def score(self, x, cmv=False):
        """
        Generate anomaly score from trained Forest.
        
        Args:
            x: Testdata to score in ndarray format(numpy 2d-matrix), it should be the same dimension as training dataset.
            cmv: Check missing value in the test data. Default false.
        Returns: anomaly score value b/n 0 and 1.
        >> score = ff.score(x,cmv=True)
        """

        #self.validate_model()
        DataValidator.validate_dataset(x)
        if x.ndim < 2:
            x = x.reshape([1, x.size])
        return self.thisptr.score(x, cmv)
        #return self.thisptr.anomaly_score()

    def validate_model(self):
        if self.thisptr.is_valid() == 1:
            raise NameError("The iForest model is not yet trained.")
        if self.thisptr.is_valid() == 2:
            raise NameError("Test data not given")

    def anomaly_score(self):
        """
        Returns: Returns anomaly score from the trained model
        """
        self.validate_model()
        return self.thisptr.anomaly_score()

    def path_length(self):
        """
        Returns: Returns path length of observations in all trees used.

        """
        self.validate_model()
        return self.thisptr.path_length()

    def average_depth(self):
        """

        Returns: Average depth(path length) across all trees of the forest.
        >> ff.average_depth() # returns average depth of all point passed in score method.
        """
        self.validate_model()  # check
        return self.thisptr.average_depth()

    def save(self, model_name=None, binary=True):
        """
        Save trained Isolation Forest model as binary or json.
        Args:
            model_name: model to save e.g. forest.bin or forest.json
            binary: bool, if true save as binary else as JSON
        Returns:

        """

        if model_name is None:
            raise ValueError("Provide file name to save")
        cdef string cppstring = model_name.encode('UTF-8')
        return self.thisptr.save(cppstring, binary)
    @classmethod
    def load(cls, model_name, forest_type="iforest", binary=True):
        """
        Load trained iForest model from JSON/binary file
        Args:
            model_name: path to the JSON/binary saved model.
            forest_type: type of trained model. Default iforest
            binary: bool if true load from binary or from JSON
        Returns: Loads a trainded iForest model from saved file.

        """

        DataValidator.validate_file_exists(model_name)
        cdef string model_name_str = model_name.encode("UTF-8")
        iforest_model = IsolationForest()
        iforest_model.thisptr.load(model_name_str, binary)
        return iforest_model

    def get_ntree(self):
        """

        Returns: number of trees used for building the forest

        """
        self.validate_model()
        return self.thisptr.num_trees()

    def get_nsample(self):
        """

        Returns: sample size used for training

        """
        self.validate_model()
        return self.thisptr.num_sample()

    def get_max_depth(self):
        """
        Returns: Maximum depth of the trees

        """
        self.validate_model()
        return self.thisptr.max_height()

    def is_adaptive(self):
        """
        Return: True if the Forest is built with adaptive way
        """
        self.validate_model()
        self.thisptr.adaptive()

    def is_range_check(self):
        """

        Returns: True if rangeCheck is set during scoring

        """
        self.validate_model()
        return self.thisptr.range_check()

    def is_rotate(self):
        """

        Returns: True if rotation forest is used

        """
        self.validate_model()
        return self.thisptr.rotate()

    def is_valid_model(self):
        """

        Returns: True if the model is valid

        """
        return self.thisptr.is_valid()

    def display_data(self, df):
        """

        Returns: displays the training data used.

        """
        #assert isinstance(df, np.ndarray)
        return self.thisptr.display_data(df)

    def explanation(self, x):
        """
        Args:
            x instance for explanation. 
        Return: Explanations 

        """
        self.validate_model()
        return self.thisptr.explanation(x)

cdef class IsolationTree:
    cdef Tree * thisptr
    cdef list train_points

    def __cinit__(self):
        self.thisptr = new Tree()
        self.train_points = []

    def __dealloc__(self):
        del self.thisptr
    def iTree(self, train_index, train_data, height=0, maxheight=0, stopheight=False,column_subsample=[]):
        """
         Args:

        :train_index: list of index of samples used for training tree
        :param train_data: ndarray training data
        :param height: Current depth of tree. Root is 0.
        :param maxheight: Maximum depth to grow. Default 0, means grow trees to full depth.
        :param stopheight: Stop growing forest after a given maxheight. Default false.
        :return: Trained tree.
        """
        if len(column_subsample)<1:
            for i in range(train_data.shape[0]):
                column_subsample.append(i)

        return self.thisptr.iTree(train_index, train_data, height, maxheight, stopheight, column_subsample)


    def path_length(self, test_data, check_miss=False):
        """

        :param test_data: ndarray testing data.
        :return: Returns 1-D depth of all testing data.
        """
        assert isinstance(test_data, np.ndarray)

        if test_data.ndim<2:
            return self.thisptr.path_length(test_data, check_miss)
        else:
            return [ self.thisptr.path_length(row, check_miss) for row in test_data]
        #return self.thisptr.pathLength(test_data, check_miss)

    def explanation(self, test_data):
        """
        :param test_data: ndarray test data for explanation.
        :return: Feature explanation of test_data.
        """
        return self.thisptr.explanation(test_data)

    # def max_depth(self):
    #     """
    #     :return: Returns maximum depth.
    #     """
    #     return self.thisptr.maxTreeDepth()

    def get_nodesize(self):
        """

        :return: Number of instance in the node.
        """
        return self.thisptr.node_size()

    def get_splittingAtt(self):
        return self.thisptr.splitting_attribute()

    def get_splittingPoint(self):
        return self.thisptr.splitting_point()

    def get_depth(self):
        return self.thisptr.depth()

    def get_minAttVal(self):
        return self.thisptr.min_attribute_value()

    def get_maxAttVal(self):
        return self.thisptr.max_attribute_value()


cdef class IForest(object):
    """
    IForest version using most python code. This is used for experimenting version.
    """
    cdef int nsample, ntree, maxheight
    cdef bool rangecheck, check_miss, adaptive
    cdef list rot_trees, trees
    # cdef np.ndarray[np.float64_t, ndim=2] train_df

    def __cinit__(self, train_df=None, ntree=100, nsample=512,
                  max_height=0, adaptive=False, rangecheck=True, check_miss=True):
        self.nsample = nsample
        self.ntree = ntree
        self.rangecheck = rangecheck
        self.adaptive = adaptive
        self.maxheight = max_height
        self.check_miss = check_miss
        self.rot_trees = []
        self.trees = []
        #self.sparsity = sparsity
        if train_df is not None:
            self.train_df = train_df
            self.train(self.train_df)

    def train(self, train_df, column_subsample=[]):
        """ Train forest
        :type train_df: numpy.ndarray training dataset
        """

        assert isinstance(train_df, np.ndarray)
        nrow, ncol = train_df.shape
        if len(column_subsample)<1:
            for i in range(train_df.shape[0]):
                column_subsample.append(i)
        if self.nsample > nrow:
            self.nsample = nrow
        for tree in range(self.ntree):
            # generate rotation matrix
            sample_index = np.random.choice(nrow, self.nsample, False)
            itree = IsolationTree()
            itree.train_points = sample_index.tolist()
            itree.iTree(sample_index, train_df, height=0, maxheight=self.maxheight, stopheight=False,
            column_subsample=column_subsample)
            self.trees.append({"tree": itree})

    @property
    def ntree(self):
        return self.ntree

    @ntree.setter
    def ntree(self, value):
        self.ntree = value

    @property
    def nsample(self):
        return self.nsample

    @nsample.setter
    def nsample(self, value):
        self.nsample = value

    def depth(self, test_df, oob=False):
        #

        depth = []

        for tree_inst in self.trees:
            #rot_mat = rottree["rotmat"]
            tree = tree_inst["tree"]
            depth.append(tree.path_length(test_df))
        return depth

    def average_depth(self, test_df):
        assert isinstance(test_df, np.ndarray)
        if test_df.ndim < 2:
            # return np.mean(self.depth(test_df))
            test_df = test_df.reshape([1, test_df.size])
        avg_depth = [np.mean(self.depth(row)) for row in test_df]
        return np.array(avg_depth)

    def oob_depth(self, test_df):
        """Compute depth using the out of bag trees"""
        assert isinstance(test_df, np.ndarray)
        depth = []
        for rottree in self.trees:
            tree = rottree["tree"]
            if test_df not in tree.train_points:
                depth.append(tree.path_length(test_df))
        return (len(depth), np.mean(depth))

    def explanation(self, query_point):
        # explanation=[]
        features = defaultdict(float)
        for rottree in self.trees:
            tree = rottree["tree"]
            for index, depth_inv in tree.explanation(query_point).items():
                features[index] += depth_inv
        return features

    def score(self, test_df):
        # score of allpoints
        def bst(n): return 0.0 if (n - 1) <= 0 else (2.0 *
                                                     np.log(n - 1) + 0.5772156649) - 2.0 * (n - 1) / n
        avg_depth = self.average_depth(test_df)
        scores = np.power(2, (-1 * avg_depth / bst(self.nsample)))
        return scores

    #@staticmethod
    def save(self, model_name):
        # First save trees and rotation matrix.
        pickle.dump(self, open(model_name, 'w'))

    def load(self, model_name):
        return pickle.load(open(model_name, "r"))

class RotationForest(object):
    """
    Build Rotation Forest based on Isolation Trees
    """
    rot_trees = []

    def __init__(self, traindf=None, ntree=100, nsample=512,
                 maxheight=0, adaptive=False, rangecheck=True, sparsity=False):
        self.nsample = nsample
        self.ntree = ntree
        self.rangecheck = rangecheck
        self.adaptive = adaptive
        self.maxheight = maxheight
        self.sparsity = sparsity
        self.sample_rotation = []

    @staticmethod
    def random_rotation_matrix(n, m=None):
        if m is None:
            m = n
        A = np.random.normal(size=[n, m])
        Q, R = np.linalg.qr(A)
        M = Q.dot(np.diag(np.sign(np.diag(R))))
        if np.linalg.det(M) < 0:
            M[:, 0] = -M[:, 0]
        return M

    def train(self, traindf):
        """ Train forest"""
        assert isinstance(traindf, np.ndarray)
        nrow, ncol = traindf.shape
        if self.sparsity and ncol > 3:
            r = int(np.ceil((2 + np.sqrt(ncol) / 2)))
            self.sample_rotation = np.random.choice(ncol, r, False)

        for tree in xrange(self.ntree):
            # generate rotation matrix
            rotMat = RotationForest.random_rotation_matrix(ncol)
            rotated_data = np.dot(traindf, rotMat)
            if self.nsample > nrow or self.nsample == 0:
                self.nsample = nrow
            sample_index = np.random.choice(nrow, self.nsample, False)
            itree = IsolationTree()
            if len(self.sample_rotation) > 0:
                rotated_data = rotated_data[:, self.sample_rotation]

            itree.iTree(sample_index, rotated_data, 0, self.maxheight)
            self.rot_trees.append({"rotmat": rotMat, "tree": itree})
        return self.ntree

    def depth(self, testdf):
        depth = []

        for rottree in self.rot_trees:
            rot_mat = rottree["rotmat"]
            tree = rottree["tree"]
            # rotate data
            rotated_dt = np.dot(testdf, rot_mat)
            depth.append(tree.path_length(rotated_dt))
        return depth

    def average_depth(self, testdf):
        assert isinstance(testdf, np.ndarray)
        if len(self.sample_rotation) > 0:
            testdf = testdf[:, self.sample_rotation]
        avg_depth = [np.mean(self.depth(row)) for row in testdf]
        return np.array(avg_depth)

    def score(self, testdf):
        # score of allpoints
        def bst(n): return 0.0 if (n - 1) <= 0 else (2.0 *
                                                     np.log(n - 1) + 0.5772156649) - 2.0 * (n - 1) / n
        avg_depth = self.average_depth(testdf)
        scores = np.power(2, (-1 * avg_depth / bst(self.nsample)))
        return scores

    #@staticmethod
    def save(self, model_name):
        # First save trees and rotation matrix.
        pickle.dump(self, open(model_name, 'w'))

    def load(self, model_name):
        return pickle.load(open(model_name, "r"))


# Error flags
class DataValidator(object):
    def __init__(self):
        self.FOREST_NOT_TRAINED = 1
        self.NO_TEST_DATA = 2
        self.OK = 0

    @staticmethod
    def validate_dataset(dataset):
        """
        Error validator for input data, make sure it is 2d  numpy (ndarray) data, dataset not empty
        @param dataset: input dataset either training or testing

        """
        if type(dataset) is not np.ndarray:
            raise NameError("Dataset is not in ndarray format")
        # check for size of dataset return for 0 size
        if len(dataset) < 1:
            raise NameError("Data is empty")

    @staticmethod
    def validate_file_exists(filename):
        """
        Check if file exists or raise error
        """
        import os.path
        if os.path.isfile(filename) == False:
            raise NameError(
                filename, "  doesn't exist make sure to specifiy correct path")
        else:
            return True

    def validate_model(error_flag):
        if error_flag == 0:  # self.OK:
            return True
        if error_flag == 1:  # self.NO_TEST_DATA:
            raise NameError(
                "No test data given to the model (test function not called)")
        if error_flag == 2:  # self.FOREST_NOT_TRAINED:
            raise NameError("train function net yet called")
