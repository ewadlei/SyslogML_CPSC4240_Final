from features import *
from model import *

logs = load_logs("training_logs.txt")

X_text, vectorizer = extract_text_features(logs)
X_proc, encoder = encode_process(logs)
X = combine_features(X_text, X_proc)

model = train_model(X)

predictions = model.predict(X)

anomalies = sum(p == -1 for p in predictions)

print("Total logs:", len(predictions))
print("Anomalies detected:", anomalies)
