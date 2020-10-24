from sklearn import mixture
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas
import itertools
from scipy import linalg
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches

color_iter = itertools.cycle(['navy', 'c', 'cornflowerblue', 'gold', "lime",
                              'darkorange', "turquoise", "hotpink", "burlywood", "chartreuse",
                              "maroon", "peru", "dodgerblue", "magenta", "crimson"])

#Plots Confidence Ellipsoids for the Gaussians obtained with EM.
def plot_results(X, Y_, means, covariances, index, title):
    splot = plt.subplot(2, 1, 1 + index)
    for i, (mean, covar, color) in enumerate(zip(
            means, covariances, color_iter)):
        v, w = linalg.eigh(covar)
        v = 2. * np.sqrt(2.) * np.sqrt(v)
        u = w[0] / linalg.norm(w[0])
        # as the DP will not use every component it has access to
        # unless it needs it, we shouldn't plot the redundant
        # components.
        if not np.any(Y_ == i):
            continue
        plt.scatter(X[Y_ == i, 0], X[Y_ == i, 1], .8, color=color)

        # Plot an ellipse to show the Gaussian component
        angle = np.arctan(u[1] / u[0])
        angle = 180. * angle / np.pi  # convert to degrees
        ell = patches.Ellipse(mean, v[0], v[1], 180. + angle, color=color)
        ell.set_clip_box(splot.bbox)
        ell.set_alpha(0.5)
        splot.add_artist(ell)

    plt.xlim(-5., 5.)
    plt.ylim(-3., 6.)
    plt.xticks(())
    plt.yticks(())
    plt.title(title)


consolidated_data = pandas.read_csv('new_consolidated_data.csv', delimiter=',')

states_years = consolidated_data.iloc[:, 0:1]

features = consolidated_data.iloc[:, 2:-13]

scaler = StandardScaler()

scaled = scaler.fit_transform(features)

gmm = mixture.GaussianMixture(n_components=15, covariance_type='full').fit_predict(scaled)
print(gmm)

gmm = mixture.GaussianMixture(n_components=15, covariance_type='full').fit(scaled)
plot_results(scaled, gmm.predict(scaled), gmm.means_, gmm.covariances_, 0, 'Gaussian Mixture')
plt.show()
