import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('reddit_data_w_summary_categories.csv')

df_obj = df.select_dtypes('object')
df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())

print(df.head())
print(df.shape)

cat1_counts = df["category1"].value_counts()

cat2_counts = df["category2"].value_counts()


cross_reference = {'bus service': ['frequency', 'punctuality', 'accessibility', 'affordability', 'quality', 'safety', 'connectivity', 'crowding', 'infrastructure/facilities'],
                  'train service': ['frequency', 'punctuality', 'accessibility', 'affordability', 'quality', 'safety', 'connectivity', 'crowding', 'infrastructure/facilities'],
                  'private transport': ['cost', 'parking', 'safety', 'traffic/congestion', 'connectivity'],
                  'walk/cycle': ['safety', 'infrastructure/facilities'],
                  'policy/regulation': ['enforcement', 'compliance', 'transparency/communication', 'impact'],
                  'other': 'other'
                  }

for cat in cross_reference:
    print(df.loc[df['category2'] == cat]["category3"].value_counts())

labels = df["category2"].value_counts().keys()
sizes = df["category2"].value_counts()
fig, ax = plt.subplots()
ax.pie(sizes, labels=labels)

