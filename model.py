from sklearn.ensemble import IsolationForest

def train_model(X):
    model = IsolationForest(contamination=0.01, random_state=42)
    model.fit(X)
    return model

