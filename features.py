from parser import parse_log
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.preprocessing import OneHotEncoder
from scipy.sparse import hstack, csr_matrix
import time
from collections import defaultdict
import numpy as np

failed_attempts = defaultdict(list)
process_activity = defaultdict(list)

def extract_behavior_features(log):
    current_time = log["timestamp"]
    msg = log["message"].lower()
    process = log["process"]

    key = "auth_fail"

    is_auth_failure = int(
            "failed password" in msg or 
            "authentication failure" in msg or
            "incorrect password" in msg or
            "incorrect password attempts" in msg
            )

    if is_auth_failure:
        failed_attempts[key].append(current_time)

    failed_attempts[key] = [
            t for t in failed_attempts[key]
            if current_time -t < 60 
    ]

    failed_count_60s = len(failed_attempts[key])
    failed_count_60s = failed_count_60s ** 2
    process_activity[process].append(current_time)

    process_activity[process] = [
            t for t in process_activity[process]
            if current_time -t < 60
    ]
    
    process_count_60s = len(process_activity[process])

    return [
            float(failed_count_60s),
            float(process_count_60s),
            float(is_auth_failure)
            ]
def load_logs(file):
    logs = []

    with open(file) as f:
        for line in f:
            parsed = parse_log(line)
            if parsed:
                logs.append(parsed)
    return logs

def extract_text_features(logs):
    messages = [log["message"] for log in logs]
    vectorizer = TfidfVectorizer(max_features=500)
    X_text = vectorizer.fit_transform(messages)

    return X_text, vectorizer

def encode_process(logs):
    processes = [[log["process"]] for log in logs]

    encoder = OneHotEncoder(handle_unknown='ignore')
    X_proc = encoder.fit_transform(processes)

    return X_proc, encoder
def combine_features(X_text, X_proc, logs):
    behavior_features = []

    for log in logs: 
        bf = extract_behavior_features(log)
        behavior_features.append(bf)

    behavior_features = np.array(behavior_features, dtype = float)
    behavior_features *= 200
    X_behavior = csr_matrix(behavior_features)

    return hstack([X_text, X_proc, X_behavior])
