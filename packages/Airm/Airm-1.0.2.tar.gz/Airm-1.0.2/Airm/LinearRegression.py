import numpy as np
from logging import error


class Regression(object):
    def __init__(self, x, y):
        if not isinstance(x, np.ndarray) or not isinstance(y, np.ndarray):
            error(": Input must be Numpy Array")
            exit(1)
        self.x = x
        self.y = y
        self.weight = []

    def train(self, log=False):
        if log:
            print("Iteration", "Error\t", "Bias", "\tWeight", sep="\t")
        x = np.insert(self.x, 0, 1, axis=1)
        theta = np.zeros(x.shape[1])
        m = self.y.size
        print_interval = change = lr = old_error = 1
        count = 0

        while abs(change) > 0.0001 and count < 1e6:
            h = (x @ theta)
            error = ((self.y - h) ** 2).mean()
            theta = theta - lr * (1 / m) * (x.T.dot(h - self.y)).reshape(-1)
            if not count % print_interval and log:
                print_interval *= 4
                print(str(count).center(10), str(round(error, 3)).center(10), round(theta[0], 4), sep="\t", end="\t")
                print(np.round(theta[1:], 2))
            change = error - old_error
            if change > 10:
                lr /= 4
            count += 1
            old_error = error
        self.weight = theta

    def predict(self, x):
        if len(x.shape) > 1:
            x = np.insert(x, 0, 1, axis=1)
        else:
            x = np.insert(x, 0, 1, axis=0)
        h = (x @ self.weight)
        return h

    def __str__(self):
        return f"Linear Regression :features {len(self.x[0])}"

    def __repr__(self):
        return self.__str__()

