import numpy as np


class NonLinerRegression(object):
    def __init__(self, feature, label, degree=0, lr=0.0001, epoch=4000):
        self.label = label
        self.lr = lr
        self.degree = degree
        self.epoch = epoch
        self.label = self.label.reshape(-1, 1)
        self.feature = self.make_array(feature)
        self.original_shape = self.feature.shape
        self.feature = self.increseDegree(self.feature)
        self.feature = np.insert(self.feature, 0, 1, axis=1)
        self.weights = np.ones(self.feature.shape[1])
        self.state = True

    def make_array(self, data):
        return data.reshape(-1, 1) if len(data.shape) < 2 else data

    def increseDegree(self, data):
        temp = self.degree
        while temp > 0:
            if data.shape[1] > temp:
                data = np.concatenate([data, data[:, :temp]], axis=1)
                temp = 0
            else:
                temp -= data.shape[1]
                data = np.concatenate([data, data], axis=1)
        for i in range(data.shape[1] - self.original_shape[1]):
            data[:, self.original_shape[1] + i] = data[:, self.original_shape[1] + i] ** (i + 2)
        return data

    def train(self, log=False):
        counter = 0
        old_error = 0
        while True:
            counter += 1
            h = np.dot(self.feature, self.weights).reshape(-1, 1)
            error = ((self.label - h) ** 2).mean()
            change = old_error - error
            if change < -1:
                self.lr /= 2
            self.weights = self.weights - (
                    self.lr * 1 / self.feature.shape[0] * ((h - self.label).T @ self.feature)).reshape(-1)
            if abs(change) < 0.00001 or counter == 2e5:
                break
            old_error = error
        if log:
            print("Error => ", error)

    def predict(self, inputs, out=True):
        if out:
            inputs = self.make_array(inputs)
            inputs = self.increseDegree(inputs)
            inputs = np.insert(inputs, 0, 1, axis=1)
        return np.dot(inputs, self.weights)

    def __str__(self):
        return f"Non - Linear Regression :features {len(self.feature[0])}"

    def __repr__(self):
        return self.__str__()
