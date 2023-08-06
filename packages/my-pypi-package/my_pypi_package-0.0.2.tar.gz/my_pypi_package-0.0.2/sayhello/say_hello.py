import numpy as np
import requests


def hello_world():
    print('hello world!')


def get_numpy():
    matrix_a = np.random.randn(3, 3)
    return matrix_a


def get_requests():
    r = requests.get('https://www.google.com')
    return r.content


if __name__ == '__main__':
    hello_world()
    print(get_numpy())
    print(get_requests())
