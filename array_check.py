import numpy as np

class ArrayCheck:
    def __init__(self, array):
        self.array = np.array(array)
        self.shape = self.array.shape
        self.size = self.array.size
        self.dtype = self.array.dtype

    def check_shape(self, expected_shape):
        return self.shape == expected_shape

    def check_size(self, expected_size):
        return self.size == expected_size

    def check_dtype(self, expected_dtype):
        return self.dtype == expected_dtype
if __name__ == "__main__":
    ac = ArrayCheck([[1, 2, 3], [4, 5, 6],  [7, 8, 9]])
    print("Shape check:", ac.check_shape((3, 3)))
    print("Size check:", ac.check_size(9))
    print("Dtype check:", ac.check_dtype(np.int64))
