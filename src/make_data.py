import pandas as pd
from datetime import datetime

df = pd.read_csv('https://query.data.world/s/tt5efa64gl6ruwmxz4wdgmhfwroi4r',
                 usecols=['longitude', 'latitude', 'region', 'admin1', 'location',
                          'event_type', 'fatalities', 'event_date'])

print('Loading in dataset from data.world/makeovermonday/2018w34-visualizing-conflict...')

df['event_type'] = ['Battle' if e[:6] == 'Battle' else e
                    for e in df['event_type']]

df['event_date'] = [datetime.strptime(d, "%d-%b-%y") for d in df['event_date']]
df['year_month'] = [str(d.year) + '_' + str(d.month) for d in df['event_date']]

df['region'] = [r if r == 'Middle East' else r.split()[1] for r in df['region']]

df.to_csv('data/world_conflict.csv', index=False)