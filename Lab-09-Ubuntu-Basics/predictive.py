import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 1. Load data
data = pd.read_csv('historical_logs.csv')

# 2. Prepare features and target
X = data[['error_count', 'warning_count', 'info_count']]
y = data['failure_occurred']

# 3. Train model (Langsung pakai semua data karena data terlalu sedikit untuk di-split)
model = RandomForestClassifier(n_estimators=10)
model.fit(X, y)

# 4. Evaluate (Cek akurasi pada data yang sama)
predictions = model.predict(X)
print(f"Model Accuracy on Train Data: {accuracy_score(y, predictions):.2f}")

# 5. Make prediction (Gunakan DataFrame agar tidak muncul warning)
new_data = pd.DataFrame([[10, 15, 70]], columns=['error_count', 'warning_count', 'info_count'])
result = model.predict(new_data)

print(f"Failure prediction: {'Yes' if result[0] == 1 else 'No'}")



