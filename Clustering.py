import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN, KMeans
from sklearn.impute import SimpleImputer

# Import data
data = pd.read_csv(r'Data\Final Data.csv')
data = data.drop_duplicates()
data = data.dropna()

# Aggregate data 
fantasy_df = data.groupby(['Player']).agg({'Cost': ['mean'],
                                           'Sel.': ['mean'],
                                           'Form': ['mean'],
                                           'Pts.': ['mean'],
                                           'Bonus': ['mean'],
                                           'Bonus Points System': ['max'],
                                           'Times in Dream Team': ['max'],
                                           'Transfers in': ['mean'],
                                           'Transfers out': ['mean'],
                                           'Price rise': ['mean']})

# Pass data to numpy array
fantasy = fantasy_df.to_numpy()

# # Imputation (if needed)
# imp = SimpleImputer(missing_values=np.nan, strategy='median')
# fantasy = imp.fit_transform(fantasy)

# Scale
scaler = StandardScaler()
fantasy = scaler.fit_transform(fantasy)

# Conduct PCA analysis for dimensionality reduction
pca = PCA(n_components=2)
fantasy = pca.fit_transform(fantasy)

# In K-Means we are required to define the desired number of clusters.
# So, we'll first try to detect the optimal number of clusters by plotting a learning curve

# Create an empty list to which we'll pass the sum of squared error within each cluster
distortions = []

# Iterate through number of clusters ranging from 1 to 10 and pass the sum of squared error of each to distortions list
for i in range(1, 11):
    km = KMeans(n_clusters=i,
                init='k-means++',
                n_init=10,
                max_iter=300,
                random_state=0)
    km.fit(fantasy)
    distortions.append(km.inertia_)

# Plot the learning curve
plt.plot(range(1, 11), distortions, marker='o', alpha=0.75)
plt.xlabel('Number of clusters')
plt.ylabel('Distortions')
plt.show()

# Now, we'll choose the final number of clusters we desire and conduct the actual clustering and visualizations
clusters_num = 4

# Initialize the K-Means object and fit predict the fantasy
km = KMeans(n_clusters=clusters_num,
            init='k-means++',
            n_init=10,
            max_iter=300,
            tol=1e-04,
            random_state=0)

km_clusters = km.fit_predict(fantasy)

# Plot PCA with clusters

# Set colors and country names
km_fig, km_ax = plt.subplots()
km_fig.set_size_inches(12, 6.7)
colors = ['lightgreen', 'orange', 'lightblue', 'salmon', 'MediumPurple1', 'brown1', 'VioletRed1']
names = pd.Series(fantasy_df.index)

# Scatter plot
for i in range(0, clusters_num):
    plt.scatter(fantasy[km_clusters == i, 0],
                fantasy[km_clusters == i, 1],
                cmap='Paired',
                label='Cluster' + str(i+1))

# Add country name to each point
for j, name in names.iteritems():
    km_ax.annotate(name, (fantasy[j][0], fantasy[j][1]), fontsize=8)

# Plot KM cetnroids
plt.scatter(km.cluster_centers_[:, 0],
            km.cluster_centers_[:, 1],
            s=85,
            alpha=0.75,
            marker='o',
            c='black',
            label='Centroids')

# Edit Legend and labels
km_ax.axes.xaxis.set_visible(False)
km_ax.axes.yaxis.set_visible(False)

# Tight layout and show
plt.tight_layout()
plt.show()

# Export plot
km_fig.savefig('Visualizations/Fantasy Clustering.png')


#######################################################################################################################


# Aggregate data 
players_df = data.groupby(['Player']).agg({'Minutes played': ['sum'],
                                           'Goals scored': ['sum'],
                                           'Assists': ['sum'],
                                           'Clean sheets': ['sum'],
                                           'Goals conceded': ['sum'],
                                           'Own goals': ['sum'],
                                           'Penalties saved': ['sum'],
                                           'Penalties missed': ['sum'],
                                           'Yellow cards': ['sum'],
                                           'Red cards': ['sum'],
                                           'Saves': ['sum'],
                                           'Player_Appearances': ['max'],
                                           'Player_NPG': ['sum'],
                                           'Player_xG': ['mean'],
                                           'Player_NPxG': ['mean'],
                                           'Player_xA': ['mean'],
                                           'Player_xGChain': ['mean'],
                                           'Player_xGBuildup': ['mean']})

# Pass data to numpy array
players = players_df.to_numpy()

# # Imputation (if needed)
# imp = SimpleImputer(missing_values=np.nan, strategy='median')
# players = imp.fit_transform(players)

# Scale
scaler = StandardScaler()
players = scaler.fit_transform(players)

# Conduct PCA analysis for dimensionality reduction
pca = PCA(n_components=2)
players = pca.fit_transform(players)

# In K-Means we are required to define the desired number of clusters.
# So, we'll first try to detect the optimal number of clusters by plotting a learning curve

# Create an empty list to which we'll pass the sum of squared error within each cluster
distortions = []

# Iterate through number of clusters ranging from 1 to 10 and pass the sum of squared error of each to distortions list
for i in range(1, 11):
    km = KMeans(n_clusters=i,
                init='k-means++',
                n_init=10,
                max_iter=300,
                random_state=0)
    km.fit(players)
    distortions.append(km.inertia_)

# Plot the learning curve
plt.plot(range(1, 11), distortions, marker='o', alpha=0.75)
plt.xlabel('Number of clusters')
plt.ylabel('Distortions')
plt.show()

# Now, we'll choose the final number of clusters we desire and conduct the actual clustering and visualizations
clusters_num = 5

# Initialize the K-Means object and fit predict the players
km = KMeans(n_clusters=clusters_num,
            init='k-means++',
            n_init=10,
            max_iter=300,
            tol=1e-04,
            random_state=0)

km_clusters = km.fit_predict(players)

# Plot PCA with clusters

# Set colors and country names
km_fig, km_ax = plt.subplots()
colors = ['lightgreen', 'orange', 'lightblue', 'salmon', 'MediumPurple1', 'brown1', 'VioletRed1']
names = pd.Series(players_df.index)

# Scatter plot
for i in range(0, clusters_num):
    plt.scatter(players[km_clusters == i, 0],
                players[km_clusters == i, 1],
                cmap='Paired',
                label='Cluster' + str(i+1))

# Add country name to each point
for j, name in names.iteritems():
    km_ax.annotate(name, (players[j][0], players[j][1]), fontsize=8)

# Plot KM cetnroids
plt.scatter(km.cluster_centers_[:, 0],
            km.cluster_centers_[:, 1],
            s=85,
            alpha=0.75,
            marker='o',
            c='black',
            label='Centroids')

# Edit Legend and labels
plt.legend(loc='best')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.tight_layout()
plt.show()


########################################                 DBSCAN              ##########################################


clusters = []
noise = []
for i in np.linspace(0.1, 5, 50):
    dbs = DBSCAN(eps=i,
                 min_samples=10)
    dbs.fit(fantasy)
    labels = dbs.labels_
    clusters.append(len(np.unique(labels)))
    noise.append(list(labels).count(-1))

# Plot the learning curve
plt.plot(np.linspace(0.1, 5, 50), clusters, marker='o', alpha=0.75)
plt.plot(np.linspace(0.1, 5, 50), noise, marker='x', alpha=0.75)
plt.xlabel('Number of clusters')
plt.ylabel('Distortions')
plt.show()

# Initialize the K-Means object and fit predict the fantasy
db = DBSCAN(eps=0.4,
            min_samples=10)

db_clusters = db.fit_predict(fantasy)

# Plot PCA with clusters

# Set colors and country names
db_fig, db_ax = plt.subplots()
names = pd.Series(fantasy_df.index)

# Scatter plot
for i in np.unique(db.labels_):
    plt.scatter(fantasy[db.labels_ == i, 0],
                fantasy[db.labels_ == i, 1],
                cmap='Paired',
                label='Cluster' + str(i+2))

# Add country name to each point
for j, name in names.iteritems():
    db_ax.annotate(name, (fantasy[j][0], fantasy[j][1]), fontsize=8)

# Edit Legend and labels
plt.legend(loc='best')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.show()
