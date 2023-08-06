from .LinearRegression import Regression
from .Non_LinearRegression import NonLinerRegression


def linear_regression(x, y):
    return Regression(x, y)


def non_linear_regression(x, y, degree=0):
    return NonLinerRegression(x,y,degree)