from parser import parse_log
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.preprocessing import OneHotEncoder
from scipy.sparse import hstack

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
def combine_features(X_text, X_proc):
    return hstack([X_text, X_proc])
