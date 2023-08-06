"""

Module to gather various high-level algorithms based on the kernel methods,
    such as kernel-based predictive models for classification and regression.

"""

from kernelmethods.base import BaseKernelFunction, KernelMatrix
from kernelmethods.sampling import KernelBucket, make_kernel_bucket
from kernelmethods.ranking import rank_kernels, find_optimal_kernel, get_estimator

from sklearn.base import BaseEstimator, RegressorMixin, ClassifierMixin
from sklearn.utils.validation import check_X_y, check_array
from sklearn.svm import SVC, SVR, NuSVC, NuSVR, OneClassSVM
from sklearn.kernel_ridge import KernelRidge
import numpy as np
import warnings

class KernelMachine(BaseEstimator):
    """Generic class to return a drop-in sklearn estimator."""

    def __init__(self,
                 k_func,
                 learner_id='SVR'):
        """Constructor"""

        self.k_func = k_func
        self.learner_id = learner_id
        self._estimator, self.param_grid = get_estimator(self.learner_id)


    def set_learner_params(self, **learner_params):
        """Separate method to set underlying estimator parameters"""

        self.learner_params = learner_params
        if len(self.learner_params) > 0:
            if 'kernel' in self.learner_params:
                warnings.warn('kernel is not allowed as parameter to estimator!'
                              'As we set it via k_func. Ignoring it!')
                self.learner_params.pop('kernel')

            # to prevent recursive parameter setting
            self.learner_params.pop('learner_params')

            valid_keys = self._estimator.get_params().keys()
            new_param_dict = {key : val for key, val in self.learner_params.items()
                              if key in valid_keys}
            self._estimator.set_params(**new_param_dict)


    def fit(self, X, y, sample_weight=None):
        """Estimate the optimal kernel, and fit a SVM based on the custom kernel.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape (n_samples, n_features)
            Training vectors, where n_samples is the number of samples
            and n_features is the number of features.
            For kernel="precomputed", the expected shape of X is
            (n_samples, n_samples).

        y : array-like, shape (n_samples,)
            Target values (class labels in classification, real numbers in
            regression)

        sample_weight : array-like, shape (n_samples,)
            Per-sample weights. Rescale C per sample. Higher weights
            force the classifier to put more emphasis on these points.

        Returns
        -------
        self : object

        Notes
        ------
        If X and y are not C-ordered and contiguous arrays of np.float64 and
        X is not a scipy.sparse.csr_matrix, X and/or y may be copied.

        If X is a dense array, then the other methods will not support sparse
        matrices as input.

        """

        self._train_X, self._train_y = check_X_y(X, y)

        self._km = KernelMatrix(self.k_func, name='train_km')
        self._km.attach_to(self._train_X)

        self._estimator.fit(X=self._km.full, y=self._train_y,
                            sample_weight=sample_weight)

        return self


    def predict(self, X):
        """
        Perform classification on samples in X.

        For an one-class model, +1 or -1 is returned.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape (n_samples, n_features)
            For kernel="precomputed", the expected shape of X is
            [n_samples_test, n_samples_train]

        Returns
        -------
        y_pred : array, shape (n_samples,)
            Class labels for samples in X.
        """


        X = check_array(X)

        # sample_one must be test data to get the right shape for sklearn X
        self._km.attach_to(sample_one=X, sample_two=self._train_X)
        test_train_KM = self._km.full
        predicted_y = self._estimator.predict(test_train_KM)

        return predicted_y
        # TODO we don't need data type conversion, as things can be
        #  different in classifiers and regressors?
        # return np.asarray(predicted_y, dtype=np.intp)


    def get_params(self, deep=True):
        """returns all the relevant parameters for this estimator!"""

        # est_param_dict = self._estimator.get_params(deep=deep)
        # est_param_dict['k_func'] = self.k_func
        # est_param_dict['learner_id'] = self.learner_id
        # est_param_dict['learner_params'] = self.learner_params
        # return est_param_dict

        return {'k_func': self.k_func,
                'learner_id' : self.learner_id}


    def set_params(self, **parameters):
        """Param setter"""

        for parameter, value in parameters.items():
            if parameter in ('k_func', 'learner_id'): # 'learner_params'
                setattr(self, parameter, value)
            # else:
            #     setattr(self._estimator, parameter, value)

        return self


class OptimalKernelSVR(SVR):
    """
    An estimator to learn the optimal kernel for a given sample and
    build a support vector regressor based on this custom kernel.

    This class is wrapped around the sklearn SVR estimator to function as its
    drop-in replacement, whose implementation is in turn based on LIBSVM.

    Parameters
    ----------

    k_bucket : KernelBucket or sampling_strategy


    Attributes
    ----------
    support_ : array-like, shape = [n_SV]
        Indices of support vectors.

    support_vectors_ : array-like, shape = [nSV, n_features]
        Support vectors.

    dual_coef_ : array, shape = [1, n_SV]
        Coefficients of the support vector in the decision function.

    coef_ : array, shape = [1, n_features]
        Weights assigned to the features (coefficients in the primal
        problem). This is only available in the case of a linear kernel.

        `coef_` is readonly property derived from `dual_coef_` and
        `support_vectors_`.

    intercept_ : array, shape = [1]
        Constants in decision function.

    """

    def __init__(self, k_bucket):

        super().__init__(kernel='precomputed')

        self.k_bucket = k_bucket


    def fit(self, X, y, sample_weight=None):
        """Estimate the optimal kernel, and fit a SVM based on the custom kernel.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape (n_samples, n_features)
            Training vectors, where n_samples is the number of samples
            and n_features is the number of features.
            For kernel="precomputed", the expected shape of X is
            (n_samples, n_samples).

        y : array-like, shape (n_samples,)
            Target values (class labels in classification, real numbers in
            regression)

        sample_weight : array-like, shape (n_samples,)
            Per-sample weights. Rescale C per sample. Higher weights
            force the classifier to put more emphasis on these points.

        Returns
        -------
        self : object

        Notes
        ------
        If X and y are not C-ordered and contiguous arrays of np.float64 and
        X is not a scipy.sparse.csr_matrix, X and/or y may be copied.

        If X is a dense array, then the other methods will not support sparse
        matrices as input.

        """

        self._train_X, self._train_y = check_X_y(X, y)

        self.opt_kernel = find_optimal_kernel(self.k_bucket,
                                              self._train_X, self._train_y,
                                              method='cv_risk')

        super().fit(X=self.opt_kernel.full, y=self._train_y,
                    sample_weight=sample_weight)

        return self


    def predict(self, X):
        """
        Perform classification on samples in X.

        For an one-class model, +1 or -1 is returned.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape (n_samples, n_features)
            For kernel="precomputed", the expected shape of X is
            [n_samples_test, n_samples_train]

        Returns
        -------
        y_pred : array, shape (n_samples,)
            Class labels for samples in X.
        """

        # sample_one must be test data to get the right shape for sklearn X
        self.opt_kernel.attach_to(sample_one=X, sample_two=self._train_X)
        test_train_KM = self.opt_kernel.full
        predicted_y = super().predict(test_train_KM)

        return predicted_y
        # TODO we don't need data type coversion, as its not classification?
        # return np.asarray(predicted_y, dtype=np.intp)

    def get_params(self, deep=True):
        """returns all the relevant parameters for this estimator!"""

        return {'k_bucket': self.k_bucket, }


    def set_params(self, **parameters):
        """Param setter"""

        for parameter, value in parameters.items():
            if parameter in ('k_bucket', ):
                setattr(self, parameter, value)
            # else:
            #     setattr(self._estimator, parameter, value)

        return self
