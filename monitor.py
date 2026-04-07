import joblib
from parser import parse_log
from scipy.sparse import hstack
import time
from collections import defaultdict
from features import *
import subprocess
import numpy as np

#load trained objexts
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")
encoder = joblib.load("encoder.pkl")

print("SyslogML monitor started... Waiting for logs")

failed_attempts.clear()
process_activity.clear()

def predict_log(log):
    msg_vec = vectorizer.transform([log["message"]])
    proc_vec = encoder.transform([[log["process"]]])

    bf = extract_behavior_features(log)
    #print("Behavior features:", bf)
    bf_scaled = np.array(bf) * 200
    bf_vec = csr_matrix([bf_scaled])

    features = hstack([msg_vec, proc_vec, bf_vec])

    pred = model.predict(features)[0]
    score = model.decision_function(features)[0]

    return pred, score, bf
proc = subprocess.Popen(
        ["journalctl", "-f", "--since", "now"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
        )
start_time = time.time()
WARMUP_SECONDS = 5
warmed_up = False

while True:
    current_time = time.time()
    if current_time - start_time < WARMUP_SECONDS:
        continue
    if current_time - start_time >= WARMUP_SECONDS and not warmed_up:
        failed_attempts.clear()
        process_activity.clear()
        service_restarts.clear()
        warmed_up = True

    line = proc.stdout.readline()

    if not line:
        continue
        
    parsed = parse_log(line)
    #print("RAW:", line)
    if not parsed:
        continue
    
    process = parsed["process"]
        
    pred, score, bf = predict_log(parsed)
    #print(f"[{process}] score={score:.3f} | {parsed['message']}")
    
    SECURITY_PROCESSES = {"sudo", "sshd", "login", "su", "systemd"}

    if (
        (pred == -1 or score < 0)
        and(
            (process in SECURITY_PROCESSES and bf[0] > 1)
            or bf[3] > 2
        )
    ):
       print(f"Alert [{process}] (score={score:.3f}): {parsed['message']}")
    time.sleep(0.2)
