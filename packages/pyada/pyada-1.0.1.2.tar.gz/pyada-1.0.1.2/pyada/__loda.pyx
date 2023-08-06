
import logging
logger = logging.getLogger(__name__)

cimport numpy
#from libc.math import isnan
cimport libc.math as cmath
import numpy as np
NA = np.nan #-9999.0

# Initial code adopted from Moy 

# utility codes. 
def nrow(x):
    if len(x.shape) == 2:
        return x.shape[0]
    return None
def ncol(x):
    if len(x.shape) == 2:
        return x.shape[1]
    return None

def rbind(m1, m2):
    if m1 is None:
        return np.copy(m2)
    return np.append(m1, m2, axis=0)

def cbind(m1, m2):
    if len(m1.shape) == 1 and len(m2.shape) == 1:
        if len(m1) == len(m2):
            mat = np.empty(shape=(len(m1), 2))
            mat[:, 0] = m1
            mat[:, 1] = m2
            return mat
        else:
            raise ValueError("length of arrays differ: (%d, %d)" % (len(m1), len(m2)))
    return np.append(m1, m2, axis=1)

def matrix(d, nrow=None, ncol=None, byrow=False):
    """Returns the data as a 2-D matrix

    A copy of the same matrix will be returned if input data dimensions are
    same as output data dimensions. Else, a new matrix will be created
    and returned.

    Example:
        d = np.reshape(range(12), (6, 2))
        matrix(d[0:2, :], nrow=2, byrow=True)

    Args:
        d:
        nrow:
        ncol:
        byrow:

    Returns: np.ndarray
    """
    if byrow:
        # fill by row...in python 'C' fills by the last axis
        # therefore, data gets populated one-row at a time
        order = 'C'
    else:
        # fill by column...in python 'F' fills by the first axis
        # therefore, data gets populated one-column at a time
        order = 'F'
    if len(d.shape) == 2:
        d_rows, d_cols = d.shape
    elif len(d.shape) == 1:
        d_rows, d_cols = (1, d.shape[0])
    else:
        raise ValueError("Dimensions more than 2 are not supported")
    if nrow is not None and ncol is None:
        ncol = int(d_rows * d_cols / float(nrow))
    elif ncol is not None and nrow is None:
        nrow = int(d_rows * d_cols / float(ncol))
    if len(d.shape) == 2 and d_rows == nrow and d_cols == ncol:
        return d.copy()
    if not d_rows * d_cols == nrow * ncol:
        raise ValueError("input dimensions (%d, %d) not compatible with output dimensions (%d, %d)" %
                         (d_rows, d_cols, nrow, ncol))
   # if isinstance(d, csr_matrix):
   #     return d.reshape((nrow, ncol), order=order)
    else:
        return np.reshape(d, (nrow, ncol), order=order)

def order(x, decreasing=False):
    if decreasing:
        return np.argsort(-x)
    else:
        return np.argsort(x)

def sample(x, n):
    shuffle = np.array(x)
    np.random.shuffle(shuffle)
    return shuffle[0:n]

def histogram_r(x, g1=1., g2=1., g3=-1., verbose=False):
    """Construct histograms that mimic behavior of R histogram package

    The type of histogram is 'regular', and right-open
    Note: the number of breaks is being computed as in:
    L. Birge, Y. Rozenholc, How many bins should be put in a regular histogram? 2006
    """

    # compute the number of bins based on the formula used by R package
    n = len(x)

    #print np.argwhere(np.isnan(x))

    nbinsmax = int(g1 * (n ** g2) * (np.log(n) ** g3))
    if verbose:
        logger.debug("max bins: %d" % (nbinsmax,))
    # density, breaks = np.histogram(x, bins=nbinsmax, density=True)

    # the below implements Birge technique that recomputes the bin sizes...
    # np.histogram are the bottleneck for computation. TODO: Remove or update the histograms
    y = np.sort(x)
    likelihood = np.zeros(nbinsmax, dtype=float)
    pen = np.arange(1, nbinsmax + 1, dtype=float) + ((np.log(np.arange(1, nbinsmax + 1, dtype=float))) ** 2.5)
    for d in range(1, nbinsmax + 1):
        # counts, breaks = np.histogram(x, bins=(y[0] + (np.arange(0, d+1, dtype=float)/d) * (y[n-1]-y[0])),
        #                              density=False)
        counts, breaks = np.histogram(x, bins=d, density=False)
        #np.his
        density = counts / (n * (breaks[1] - breaks[0]))
        like = np.zeros(d, dtype=float)
        like2 = np.zeros(d, dtype=float)
        tmp = np.where(counts > 0)[0]
        if len(tmp) > 0:
            like2[tmp] = np.log(density[tmp])
        like[np.isfinite(like2)] = like2[np.isfinite(like2)]
        likelihood[d - 1] = np.sum(counts * like)
        if np.min(counts) < 0:
            likelihood[d - 1] = -np.Inf
    penlike = likelihood - pen
    optd = np.argmax(penlike)
    if verbose:
        logger.debug("optimal num bins: %d" % (optd + 1,))

    counts, breaks = np.histogram(x, bins=optd + 1, density=False)
    density = counts / (n * (breaks[1] - breaks[0]))

    hist = HistogramR(counts=np.array(counts, float), density=np.array(density, float),
                      breaks=np.array(breaks, dtype=float))
    return hist

def pdf_hist_equal_bins(x, h, minpdf=1e-8):
    # here we are assuming a regular histogram where
    # h.breaks[1] - h.breaks[0] would return the width of the bin
    p = (x - h.breaks[0]) / (h.breaks[1] - h.breaks[0])
    ndensity = len(h.density)
    p = np.array([min(int(np.trunc(v)), ndensity-1) for v in p])
    d = h.density[p]
    # quick hack to make sure d is never 0
    d = np.array([max(v, minpdf) for v in d])
    return d



cdef class HistogramR(object):
     cdef public numpy.ndarray counts
     cdef public numpy.ndarray breaks
     cdef public numpy.ndarray density
     def __cinit__(self, counts, density, breaks):
        self.density = density
        self.counts = counts
        self.breaks = breaks

        
cdef int get_bin_for_equal_hist(double* breaks, double x, int m) nogil:
    if cmath.isnan(x):
        return 0
    if x<breaks[0]:
        return 0
    if x > breaks[m-1]:
        return m-1
    #with gil:
    cdef int i = <int>cmath.floor((x - breaks[0]) / (breaks[1] - breaks[0]))  # get integral value
    return i

cdef double cmax(double x, double y) nogil:
    if x>y:
        return x
    else:
        return x

cdef numpy.ndarray pdf_hist_w(numpy.ndarray x, int n, HistogramR h, double minpdf, numpy.ndarray pd):
                              #numpy.ndarray breaks, numpy.ndarray density, double minpdf, numpy.ndarray pd):

    cdef double* hist_break = <double*> h.breaks.data
    cdef double* hist_den = <double*> h.density.data
    cdef int hist_size = h.breaks.shape[0]
    cdef int hist_den_size = h.density.shape[0]
    cdef int i

    cdef double* _x = <double*> x.data


    #cdef numpy.ndarray pd = np.zeros(n)
    cdef double* _pd = <double*> pd.data
    if n>1:
        #with nogil:

        for j in range(n):
        #for i in prange(n, nogil=True):
            # use simple index lookup in case the histograms are equal width
            # this returns the lower index
            i = get_bin_for_equal_hist(hist_break, x[j], hist_size)
            if i >= hist_den_size:
                i = hist_den_size-1  # maybe something else should be done here
            _pd[j] = cmax(hist_den[i], minpdf)
    else:
         #x = (double*)x

         i = get_bin_for_equal_hist(hist_break, x, hist_size)
         if i >= hist_den_size:
             i = hist_den_size - 1
         _pd[0] = cmax(hist_den[i], minpdf)
    return pd


cpdef pdf_hist(x, HistogramR h, double minpdf=1e-8):

    #pdf_hist(x, h.breaks, h.density, minpdf)

    if type(x) is not numpy.ndarray:
        x = np.array(x) #double:

    cdef int n = x.size
    cdef numpy.ndarray pd = np.zeros(n)

    #with nogil:
    return pdf_hist_w(x, n, h, minpdf, pd)


cdef all_hist_pdfs_miss(numpy.ndarray a, list hists, numpy.ndarray w, int n):
    cdef numpy.ndarray miss_column = np.where(np.isnan((a)))[0]
    cdef numpy.ndarray hpdfs = np.zeros(shape=(n))
    if miss_column.size > 0:

        w_miss = w[miss_column, :]
        idx_miss = np.where(~ np.any(w_miss, axis=0))[0] #.tolist()
        #print len(idx_miss), " Number of available projects"
        temp = a.copy()  ## small hack to replace nan with any number because nan*0 doesn't give real number.
        temp[np.isnan(temp)] = -9999999999999.0
        if len(idx_miss)<1:
            return hpdfs
        x = np.dot(temp, w[:,idx_miss])

        for ix, ihist in enumerate(idx_miss):
            hpdfs[ihist] = pdf_hist(x[ix], hists[ihist])
    else:
        x = np.dot(a,w) #a.dot(w)
        for ihist in range(0,n):
            hpdfs[ihist] = pdf_hist(x[ihist], hists[ihist])
    return hpdfs


cpdef numpy.ndarray cy_get_all_hist_pdfs_miss(numpy.ndarray a, numpy.ndarray w, list hists):
    cdef int  a_c = a.shape[0], hist_len = len(hists)
    # x = a.dot(w)
    cpdef numpy.ndarray hpdfs = np.zeros(shape=(len(a), len(hists)), dtype=float)
    cdef numpy.ndarray x
    cdef numpy.ndarray miss_column
    for i in range(0, a_c):
        hpdfs[i,:]= all_hist_pdfs_miss(a[i,:], hists, w, hist_len)
    return hpdfs

def histogram_r(x, g1=1., g2=1., g3=-1., verbose=False):
    """Construct histograms that mimic behavior of R histogram package

    The type of histogram is 'regular', and right-open
    Note: the number of breaks is being computed as in:
    L. Birge, Y. Rozenholc, How many bins should be put in a regular histogram? 2006
    """

    # compute the number of bins based on the formula used by R package
    n = len(x)

    #print np.argwhere(np.isnan(x))

    nbinsmax = int(g1 * (n ** g2) * (np.log(n) ** g3))
    if verbose:
        logger.debug("max bins: %d" % (nbinsmax,))
    # density, breaks = np.histogram(x, bins=nbinsmax, density=True)

    # the below implements Birge technique that recomputes the bin sizes...
    y = np.sort(x)
    likelihood = np.zeros(nbinsmax, dtype=float)
    pen = np.arange(1, nbinsmax + 1, dtype=float) + ((np.log(np.arange(1, nbinsmax + 1, dtype=float))) ** 2.5)
    for d in range(1, nbinsmax + 1):
        # counts, breaks = np.histogram(x, bins=(y[0] + (np.arange(0, d+1, dtype=float)/d) * (y[n-1]-y[0])),
        #                              density=False)
        counts, breaks = np.histogram(x, bins=d, density=False)
        #np.his
        density = counts / (n * (breaks[1] - breaks[0]))
        like = np.zeros(d, dtype=float)
        like2 = np.zeros(d, dtype=float)
        tmp = np.where(counts > 0)[0]
        if len(tmp) > 0:
            like2[tmp] = np.log(density[tmp])
        like[np.isfinite(like2)] = like2[np.isfinite(like2)]
        likelihood[d - 1] = np.sum(counts * like)
        if np.min(counts) < 0:
            likelihood[d - 1] = -np.Inf
    penlike = likelihood - pen
    optd = np.argmax(penlike)
    if verbose:
        logger.debug("optimal num bins: %d" % (optd + 1,))

    counts, breaks = np.histogram(x, bins=optd + 1, density=False)
    density = counts / (n * (breaks[1] - breaks[0]))

    hist = HistogramR(counts=np.array(counts, float), density=np.array(density, float),
                      breaks=np.array(breaks, dtype=float))
    return hist

def pdf_hist_equal_bins(x, h, minpdf=1e-8):
    # here we are assuming a regular histogram where
    # h.breaks[1] - h.breaks[0] would return the width of the bin
    p = (x - h.breaks[0]) / (h.breaks[1] - h.breaks[0])
    ndensity = len(h.density)
    p = np.array([min(int(np.trunc(v)), ndensity-1) for v in p])
    d = h.density[p]
    # quick hack to make sure d is never 0
    d = np.array([max(v, minpdf) for v in d])
    return d


class ProjectionVectorsHistograms(object):
    def __init__(self, w=None, hists=None):
        """

        Args:
            w: numpy.ndarray(dtype=int)
            hists: list of HistogramR
        """
        self.w = w
        self.hists = hists

class LodaModel(object):
    def __init__(self, k=0, pvh=None, sigs=None):
        """
        Args:
            k: int
            pvh: ProjectionVectorsHistograms
            sigs: numpy.array(dtype=float)
        """
        self.k = k
        self.pvh = pvh
        self.sigs = sigs

class LodaResult(object):
    def __init__(self, anomranks=None, nll=None, pvh=None):
        """

        Args:
            anomranks: numpy.array(dtype=int)
            nll: numpy.array(dtype=float)
            pvh: LodaModel
        """
        self.anomranks = anomranks
        self.nll = nll
        self.pvh = pvh

class Loda(object):
    def __init__(self, train_x=None, sparsity=np.nan, mink=1, maxk=0,
    keep=None, exclude=None, original_dims=False):
        self.sparsity = sparsity
        self.mink = mink
        self.maxk = maxk
        self.keep = keep
        self.exclude = exclude
        self.original_dims = original_dims
        self.fitted = False 
        if train_x is not None:
            self.train(train_x)
        
        
    def get_random_proj(self, nproj, d, sp, keep=None, exclude=None):
        nzeros = int(np.floor(d * sp))
        idxs = np.arange(d)  # set of dims that will be sampled to be set to zero
        marked = []
        if keep is not None:
            marked.extend(keep)
        if exclude is not None:
            # since 'exclude' contains the dims that are
            # predetermined to be zero, adjust the number
            # of zero dims that need to be further determined
            # by sampling
            nzeros -= len(exclude)
            marked.extend(exclude)
        if len(marked) > 0:
            # remove from the known set -- the dims that have been
            # marked for keeping or excluding. There is no uncertainty in
            # the selection/rejection of marked dims.
            idxs = np.delete(idxs, marked)
        w = np.zeros(shape=(d, nproj), dtype=float)
        for i in range(nproj):
            w[:, i] = np.random.randn(d)
            if nzeros > 0:
                z = sample(idxs, min(nzeros, len(idxs)))
                # shuffle = np.array(idxs)
                # np.random.shuffle(shuffle)
                # z = shuffle[0:min(nzeros, len(idxs))]
                if exclude is not None:
                    z.extend(exclude)
                w[z, i] = 0
            w[:, i] = w[:, i] / np.sqrt(sum(w[:, i] * w[:, i]))

        return w

    def build_proj_hist(self, a, w):
        d = ncol(w)  # number of columns
        x = a.dot(w)
        hists = []
        for j in range(d):
            hists_j = histogram_r(x[:, j])
            hists.append(hists_j)
        return hists

    def get_neg_ll(self, a, w, hist, inf_replace=np.nan):
        x = a.dot(w)
        pdfs = np.zeros(shape=(len(x), 1), dtype=float)
        pdfs[:, 0] = pdf_hist_equal_bins(x, hist)
        pdfs[:, 0] = np.log(pdfs)[:, 0]
        if inf_replace is not np.nan:
            pdfs[:, 0] = [max(v, inf_replace) for v in pdfs[:, 0]]
        return -pdfs  # neg. log-lik of pdf

    # get all pdfs from individual histograms.
    def get_all_hist_pdfs(self, a, w, hists):
        x = a.dot(w)
        hpdfs = np.zeros(shape=(len(x), len(hists)), dtype=float)
        for i in range(len(hists)):
            hpdfs[:, i] = pdf_hist(x[:, i], hists[i])
        return hpdfs


    # Compute negative log-likelihood using random projections and histograms
    def get_neg_ll_all_hist(self, a, w, hists, inf_replace=np.nan, check_miss=False):
        if check_miss:
            pds = self.get_all_hist_pdfs_miss(a, w, hists)
        else:
            pds = self.get_all_hist_pdfs(a, w, hists)
        ll = self.get_score(pds, inf_replace)
        # pds = get_all_hist_pdfs(a,w,hists)
        ## Average only using the
        # pds = np.log(pds)
        # if inf_replace is not np.nan:
        #     vfunc = np.vectorize(max)
        #     pds = vfunc(pds, 1.0 * inf_replace) # [max(v, inf_replace) for v in pds[:, i]]
        # ll = -np.mean(pds, axis=1)  # neg. log-lik
        return ll

    def get_score(self, pds, inf_replace):

        #  ll_score = np.zeros_like(pds)
        # pds[0,:] = np.zeros(pds.shape[1])
        pds_log = pds.copy()
        pds_log[pds_log == 0] = 1
        pds_log = np.log(pds_log)
        # print pds
        if inf_replace is not np.nan:
            vfunc = np.vectorize(max)
            pds = vfunc(pds, 1.0 * inf_replace)  # [max(v, inf_replace) for v in pds[:, i]]
        non_zero_proj = np.count_nonzero(pds, axis=1)
        # non_zero_proj[0] =0
        non_zero_proj[non_zero_proj == 0] = 1
        # print non_zero_proj
        ll = -np.sum(pds_log, axis=1) / non_zero_proj  # -np.mean(pds, axis=1)  # neg. log-lik
        return ll

    def get_miss_features(self, test_df):
        if np.isnan(NA):
            miss_column = np.where(np.isnan(test_df))[0]
        else:
            miss_column = np.where(test_df == NA)[0]
        return miss_column
    def get_all_hist_pdfs_miss(self, a, w, hists):

        return cy_get_all_hist_pdfs_miss(a, w, hists)

    # Determine k - no. of dimensions
    # sp=1 - 1 / np.sqrt(ncol(a)),
    def get_best_proj(self, a, mink=1, maxk=10, sp=0.0, keep=None, exclude=None):
        """

        :type a: numpy.ndarray
        :type mink: int
        :type maxk: int
        :type sp: float
        """
        t = 0.01
        n = nrow(a)
        d = ncol(a)

        # if (debug) print(paste("get_best_proj",maxk,sp))
        # logger.debug("get_best_proj: sparsity: %f" % (sp,))

        w = np.zeros(shape=(d, maxk + 1), dtype=float)
        hists = []
        fx_k = np.zeros(shape=(n, 1), dtype=float)
        fx_k1 = np.zeros(shape=(n, 1), dtype=float)

        w_ = self.get_random_proj(nproj=1, d=d, sp=sp, keep=keep, exclude=exclude)
        w[:, 0] = w_[:, 0]
        hists.append(self.build_proj_hist(a, w_)[0])
        fx_k[:, 0] = self.get_neg_ll(a, w_, hists[0])[:, 0]

        sigs = np.ones(maxk) * np.Inf
        k = 0
        # logger.debug("mink: %d, maxk: %d" % (mink, maxk))
        while k <= mink or k < maxk:
            w_ = self.get_random_proj(nproj=1, d=d, sp=sp, keep=keep, exclude=exclude)
            w[:, k + 1] = w_[:, 0]
            hists.append(self.build_proj_hist(a, w_)[0])

            ll = self.get_neg_ll(a, w[:, k + 1], hists[k + 1])

            fx_k1[:, 0] = fx_k[:, 0] + ll[:, 0]

            diff_ll = abs(fx_k1 / (k + 2.0) - fx_k / (k + 1.0))
            # logger.debug(diff_ll)
            diff_ll = diff_ll[np.isfinite(diff_ll)]
            if len(diff_ll) > 0:
                sigs[k] = np.mean(diff_ll)
            else:
                raise (ValueError("Log-likelihood was invalid for all instances"))
            tt = sigs[k] / sigs[0]
            # print (c(tt, sigs[k], sigs[1]))
            # print(which(is.na(diff_ll)))
            # print(diff_ll)
            if tt < t and k >= mink:
                break

            fx_k[:, 0] = fx_k1[:, 0]

            # if (debug) print(paste("k =",k,"; length(sigs)",length(sigs),"; sigs_k=",tt))

            k += 1

        bestk = np.where(sigs == np.min(sigs))[0][0]  # np.where returns tuple of arrays
        # print "bestk: %d" % (bestk,)
        return LodaModel(bestk, ProjectionVectorsHistograms(matrix(w[:, 0:bestk], nrow=nrow(w)),
                                                            hists[0:bestk]),
                         sigs)

    def get_original_proj(self, a, maxk=10, sp=0, keep=None, exclude=None):
        d = ncol(a)
        w = np.zeros(shape=(d, d - (0 if exclude is None else len(exclude))), dtype=float)
        hists = []
        k = 0
        for l in range(d):
            if exclude is not None and len(np.where(exclude == l)[0]) > 0:
                continue
            w_ = np.zeros(shape=(d, 1), dtype=float)
            w_[l, 0] = 1  # important: the 'l'-th (not 'k'-th) dim is 1
            w[:, k] = w_[:, 0]
            hists.append(self.build_proj_hist(a, w_)[0])
            k += 1

        return LodaModel(k=k, pvh=ProjectionVectorsHistograms(w=w, hists=hists), sigs=None)


    def train(self, train_x):
        l, d = train_x.shape
        self.maxk = max(self.mink, 3*d if self.maxk ==0 else self.maxk)
        if self.sparsity is None or self.sparsity is np.nan:
            sp = 0 if d == 1 else 1 - 1/np.sqrt(d)
        else:
            sp = self.sparsity
        logger.debug("loda: sparsity: %f" % sp)
        if self.original_dims:
            pvh = self.get_original_proj(train_x,self.maxk,sp,self.keep,self.exclude)
        else:
            pvh = self.get_best_proj(train_x,self.mink,self.maxk,sp,self.keep,self.exclude)
        self.fitted = True
        self.pvh = pvh
    def score(self, test_x, check_miss=False):
        if not self.fitted:
            raise ValueError("The Loda model is not trained. Use train() to train.")
        nll = self.get_neg_ll_all_hist(test_x, self.pvh.pvh.w, self.pvh.pvh.hists, inf_replace = np.nan, check_miss = check_miss)
        anom_ranks = np.arange(nrow(test_x))
        anom_ranks = anom_ranks[order(-nll)]
        return nll #LodaResult(anomranks=anom_ranks, nll=nll, pvh=self.pvh)


