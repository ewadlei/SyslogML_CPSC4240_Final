import joblib
from parser import parse_log
from scipy.sparse import hstack
import time
from collections import defaultdict
from features import *
import subprocess

#load trained objexts
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")
encoder = joblib.load("encoder.pkl")

print("SyslogML monitor started... Waiting for logs")

def predict_log(log):
    msg_vec = vectorizer.transform([log["message"]])
    proc_vec = encoder.transform([[log["process"]]])

    bf = extract_behavior_features(log)
    print("Behavior features:", bf)

    bf_vec = csr_matrix([bf])
    features = hstack([msg_vec, proc_vec, bf_vec])

    pred = model.predict(features)[0]
    score = model.decision_function(features)[0]

    return pred, score
proc = subprocess.Popen(
        ["journalctl", "f"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
        )
while True:
    line = proc.stdout.readline()

    if not line:
        continue
        
    parsed = parse_log(line)
    print(parsed)
    if not parsed:
        continue
    
    process = parsed["process"]
        
    pred, score = predict_log(parsed)
    print(f"[{process}] score={score:.3f} | {parsed['message']}")

    if pred == -1 or score < -0.02:
        print(f"Alert [{process}] (score={score:.3f}): {parsed['message']}")
    time.sleep(0.2)
