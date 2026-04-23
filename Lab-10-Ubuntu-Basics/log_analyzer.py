from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Sample logs (replace with real logs)
logs = ["ERROR: Disk full", "INFO: Backup completed", "ERROR: Permission denied"]
labels = np.array([1, 0, 1])  # 1=error, 0=info

# Preprocess
tokenizer = Tokenizer(num_words=100)
tokenizer.fit_on_texts(logs)
sequences = tokenizer.texts_to_sequences(logs)

# Train a simple model
model = Sequential([
    Dense(10, activation='relu'),
    Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy')
model.fit(np.array(sequences), labels, epochs=5)

# Predict
# Ganti bagian prediksi lama Anda dengan ini
test_log = ["ERROR: Connection failed"]
test_seq = tokenizer.texts_to_sequences(test_log)

# Tambahkan baris pad_sequences ini! 
# Sesuaikan 'maxlen' dengan panjang yang digunakan saat training (biasanya 3)
test_seq_padded = pad_sequences(test_seq, maxlen=3) 

print("Prediction:", model.predict(test_seq_padded))


