import pandas as pd
from pyod.models.knn import KNN
import matplotlib.pyplot as plt

# Load log data
df = pd.read_csv('system_logs.csv')

# Feature engineering: convert log_level to numerical values
df['log_level_num'] = df['log_level'].map({'INFO':0, 'WARNING':1, 'ERROR':2})

# Train anomaly detection model
clf = KNN(n_neighbors=2)
clf.fit(df[['log_level_num', 'count']])

# Predict anomalies
df['anomaly'] = clf.predict(df[['log_level_num', 'count']])

# Visualize results
plt.scatter(df['count'], df['log_level_num'], c=df['anomaly'], cmap='cool')
plt.xlabel('Log Count')
plt.ylabel('Log Level (0=INFO, 1=WARNING, 2=ERROR)')
plt.title('Anomaly Detection in System Logs')
plt.show()
print(df)


