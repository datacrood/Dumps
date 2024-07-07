import pandas as pd

df = pd.read_csv('/Users/deveshsharma/Downloads/my-dashboard/public/dataO.csv')
df = df.sample(frac=0.1, random_state=1)
df.to_csv('data1.csv', index=False)