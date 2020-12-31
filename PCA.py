import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Import StandartScaler
scaler = StandardScaler()

# Creating a list of the categories we'll apply pca analysis on
cov_ctg_lst = ['cases', 'deaths', 'tests', 'positive_rate', 'stringency', 'reproduction']
mob_ctg_lst = ['cases', 'deaths', 'tests', 'positive_rate', 'stringency', 'reproduction']

# Creating a final dataframe to append the results to
final = pd.DataFrame(columns=['country'] + ctg_lst)

# Iterate on the different categories and apply the analysis
for category in ctg_lst:
    scaler = StandardScaler()

    # Import data
    df = pd.read_excel(r'C:\Users\nirgo\Documents\GitHub\Fiscal_Multipliers\פרק ו\תכניות הקורונה הממשלתיות\השוואה בינל - קורונה.xlsx', sheet_name=category)

    # Scale
    scaler.fit(df.drop(columns='Abbreviation'))
    data = scaler.transform(df.drop(columns='Abbreviation'))

    # Fit
    pca = PCA(n_components=1)
    pca.fit(data)
    x_pca = pd.DataFrame(pca.transform(data))

    # Append to the final df
    final[category] = x_pca[0]

final['country'] = df['Abbreviation']

final.to_csv(r'C:\Users\nirgo\Documents\GitHub\Fiscal_Multipliers\פרק ו\תכניות הקורונה הממשלתיות\PCA.csv', index=False)