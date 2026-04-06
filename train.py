from features import *
from model import *
import joblib

failed_attempts.clear()
process_activity.clear()

#load logs 
logs = load_logs("clean_logs.txt")
logs = sorted(logs, key=lambda x: x["timestamp"])

#Extract features
X_text, vectorizer = extract_text_features(logs)
X_proc, encoder = encode_process(logs)
X= combine_features(X_text, X_proc, logs)

#train the model 
model = train_model(X)

#save everything
joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
joblib.dump(encoder, "encoder.pkl")

print ("Training complete.")
