import pandas as pd
from datetime import datetime

df = pd.read_csv('https://query.data.world/s/tt5efa64gl6ruwmxz4wdgmhfwroi4r')

df['event_type'] = ['Battle' if e[:6] == 'Battle' else e
                    for e in df['event_type']]

df['event_date'] = [datetime.strptime(d, "%d-%b-%y") for d in df['event_date']]

df.to_csv('data/world_conflict.csv', index=False)