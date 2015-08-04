import matplotlib.pyplot as plt, pandas as pd, datetime , time
import os.path, cPickle
mc_stories = pd.DataFrame.from_csv(os.path.expanduser( '~/Downloads/mediacloud-sentence-counts-20150730152700.csv'))
st = {str(i[0])[:10]: int(i[1]['sentences']) for i in mc_stories.iterrows()}
plt.xkcd()
plt.bar(range(len(st)), [st[i] for i in sorted(st.keys())])
times = sorted(st.keys())

plt.xticks(range(len(st)), times, rotation = 90)
plt.show()
