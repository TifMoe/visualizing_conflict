import pandas as pd

df = pd.read_csv('https://query.data.world/s/tt5efa64gl6ruwmxz4wdgmhfwroi4r')
df.to_csv('data/world_conflict.csv', index=False)