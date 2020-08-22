from unittest import TestCase
from intentClassifier.prediction import Prediction


class TestPrediction(TestCase):
    def test_append(self):
        pre = Prediction('', 0.0)
        pre = pre.append('a', 0.1, 2)
        pre = pre.append('b', 0.2, 2)
        pre = pre.append('d', 0.4, 2)
        pre = pre.append('g', 0.7, 2)
        pre = pre.append('c', 0.3, 2)
        pre = pre.append('f', 0.6, 2)
        pre = pre.append('e', 0.5, 2)
        output = pre.to_list()
        self.assertEqual(
            [
                {"label": "g", "similarity": 0.7},
                {"label": "f", "similarity": 0.6}
            ],
            output
        )
        # 再加入重复
        pre = pre.append('g', 1.0, 2)
        output = pre.to_list()
        self.assertEqual(
            [
                {"label": "g", "similarity": 1.0},
                {"label": "f", "similarity": 0.6}
            ],
            output
        )

        # 深度检查
        current = pre
        depths = []
        while current:
            depths.append(current.depth)
            current = current.prev
        self.assertEqual([1, 0], depths)


