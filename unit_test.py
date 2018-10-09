import unittest
import shrinking_model
import extended_model
import multiplication_model
import numpy as np


class MyTestCase(unittest.TestCase):
    def test_shrinking_model(self):
        mat = [[0, 0, 0, 1, 0], [0, 0, 1, 1, 0], [0, 1, 0, 1, 0], [0, 0, 0, 1, 0], [0, 0, 0, 1, 0]]
        ans = '010'
        pattern = shrinking_model.get_pattern(mat)
        self.assertEqual(ans, pattern)

    def test_extended_model(self):
        mat = [[0, 0, 0, 1, 0], [0, 0, 1, 1, 0], [0, 1, 0, 1, 0], [0, 0, 0, 1, 0], [0, 0, 0, 1, 0]]
        ans = '01110'
        pattern = extended_model.get_pattern(mat)
        self.assertEqual(ans, pattern)

    def test_multiplication_model(self):
        mat = [[0, 0, 0, 1, 0], [0, 0, 1, 1, 0], [0, 1, 0, 1, 0], [0, 0, 0, 1, 0], [0, 0, 0, 1, 0]]
        mat = np.reshape(mat, (5, 5))
        ans = '010121'
        pattern = multiplication_model.get_pattern(mat)
        self.assertEqual(ans, pattern)


if __name__ == '__main__':
    unittest.main()
