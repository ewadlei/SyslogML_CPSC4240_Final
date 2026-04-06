from sklearn.svm import OneClassSVM

def train_model(X):
    model = OneClassSVM(nu=0.01, kernel='rbf', gamma='scale')
    model.fit(X)
    return model

