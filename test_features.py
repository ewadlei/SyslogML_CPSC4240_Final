from features import load_logs, extract_text_features, encode_process, combine_features

logs = load_logs("training_logs.txt")

X_text, vectorizer = extract_text_features(logs)
X_proc, encoder = encode_process(logs)

X = combine_features(X_text, X_proc)

print("Feature shape:", X.shape)
print(type(X))
print(X[0])
