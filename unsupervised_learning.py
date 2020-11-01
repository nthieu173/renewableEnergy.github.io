import numpy as np
import sklearn
from sklearn.decomposition import PCA
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import colors

# Uncomment following lines to print dataframe without truncation
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', -1)

class Unsupervised_Learning():
    def __init__(self, data_file='new_consolidated_data.csv', ncomp=0, nclusters=0, plot=True):
        self.df = pd.read_csv(data_file, sep=',', header=0)
        self.data = self.df.iloc[:,2:-13]
        print(self.data.shape)
        self.renew_percent = self.df.iloc[:,-1] / 100
        self.scaled_data = sklearn.preprocessing.scale(self.data)
        self.ncomp = ncomp
        self.nclusters = nclusters
        self.plot = plot

    def PCA(self):
        # Perform PCA on scaled features
        if self.ncomp == 0:
            pca = PCA(n_components='mle', svd_solver='full')
        else:
            pca = PCA(n_components=self.ncomp, svd_solver='full')

        pca.fit(self.scaled_data)
        self.rd_features = pca.transform(self.scaled_data)
        self.ncomp = len(pca.components_)
        idx_comp = range(1, self.ncomp + 1)
        rec_var = np.cumsum(pca.explained_variance_ratio_)

        idx_features = range(1, self.data.shape[1] + 1)
        abs_pc_vector = np.abs(pca.components_)


        if self.plot:
            # Plot variance recovered
            fig1 = plt.figure()
            plt.title(f'PCA Results - {self.ncomp} components (MLE)')
            plt.xlabel('PC')
            plt.xticks(idx_comp)
            plt.ylabel('Variance')
            plt.bar(idx_comp, pca.explained_variance_ratio_, label='variance of PC')
            plt.step(idx_comp, rec_var, where='mid', label='cumulative recovered variance')
            plt.legend(loc='best')

            fig2, ax = plt.subplots(3, 1, constrained_layout=True)
            fig2.suptitle('Magnitude of First 3 Principle Component Vectors')
            for i in range(3):
                ax[i].set_title(f'PC {i+1}')
                ax[i].set_xlabel('Feature Index')
                ax[i].set_ylabel('Magnitude')
                ax[i].bar(idx_features,abs_pc_vector[i,:])

        return

    def __call__(self, *args, **kwargs):
        self.PCA()

        plt.show()
        return


if __name__ == '__main__':
    Unsupervised_Learning()()

