class Prediction:

    def __init__(self, label: str, similarity: float):
        self.label = label
        self.similarity = similarity
        self.prev = None
        self.depth = 0

    def append(self, label: str, similarity: float, length: int):
        # 去重
        if label == self.label:
            if similarity > self.similarity:
                self.similarity = similarity
            return self
        # 小的情况
        if similarity <= self.similarity:
            # 如果没有满, 仍然可以追加
            if self.depth < (length - 1):
                younger = Prediction(label, similarity)
                younger.prev = self
                younger.depth = self.depth + 1
                return younger
            # 满了就返回自己.
            else:
                return self
        # 大的情况就一定要追加.
        # 先看有没有爹
        elif self.prev:
            elder = self.prev.append(label, similarity, length)
            # 还有空间才能追加.
            return self._with_elder(elder, length)

        # 没有爹的情况下, 先造一个
        else:
            elder = Prediction(label, similarity)
            return self._with_elder(elder, length)

    def _with_elder(self, elder, length):
        if elder.depth < (length - 1):
            self.prev = elder
            self.depth = elder.depth + 1
            return self
        # 没有空间了就只好返回
        else:
            return elder

    def to_list(self):
        output = []
        current = self
        while current:
            if current.label:
                output.insert(0, {"label": current.label, "similarity": current.similarity})
            current = current.prev
        return output
