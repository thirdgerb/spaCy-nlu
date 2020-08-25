from .prediction import Prediction


class IntentClassifier:

    def __init__(self, spacy_nlp, matched_threshold):
        self.nlp = spacy_nlp
        self.doc_map = {}
        self.label_hash_map = {}
        self.matched_threshold = matched_threshold or 0.95

    def learn(
        self,
        label: str,
        int_example: str
    ):
        """
        学习一条语料. 不去重.
        :param label:
        :param int_example:
        :return: void
        """
        label_hash = hash(label)
        self.label_hash_map[label_hash] = label
        if label not in self.doc_map:
            self.doc_map[label_hash] = []
        example_doc = self.nlp(int_example)
        if example_doc.has_vector:
            self.doc_map[label_hash].append(example_doc)

    def learn_intent(
        self,
        label: str,
        examples: list
    ):
        """
        学习一整组意图的语料
        不去重.
        :param label:
        :param examples:
        :return:
        """
        label_hash = hash(label)
        self.label_hash_map[label_hash] = label
        self.doc_map[label_hash] = []
        for example in examples:
            example_doc = self.nlp(example)
            if example_doc.has_vector:
                self.doc_map[label_hash].append(example_doc)

    def flush(self):
        self.doc_map = {}

    def predict(
        self,
        sentence_doc,
        possibles: list,
        threshold=0.7,
        limit=5
    ):
        """
        生成一个意图的预测结果.
        :param sentence_doc:  一个 nlu doc 文档
        :param possibles: 可能的意图
        :param threshold: 要求的阈值.
        :param limit: 最大数量
        :return: [{"label": "", "similarity": 0.0}]
        """
        pred = Prediction("", 0.0)
        # 浅拷贝, 不要相互干扰
        doc_map = self.doc_map.copy()
        # 完全命中的阈值. 遇到这个阈值的直接返回.
        matched_threshold = self.matched_threshold

        possibles_hashes = []
        for possible in possibles:
            possible_hash = hash(possible)
            possibles_hashes.append(possible_hash)

        # 先执行 possible 的检查.
        for label_hash in possibles_hashes:
            # 没有语料
            if label_hash not in doc_map:
                continue
            # 循环查找.
            doc_list = doc_map[label_hash]
            # 删除掉元素, 等下还可能要遍历.
            del doc_map[label_hash]
            for doc in doc_list:
                s = doc.similarity(sentence_doc)
                if s >= threshold:
                    label = self.label_hash_map[label_hash]
                    pred = pred.append(label, s, limit)
                # 有认为命中的阈值, 直接返回
                if s >= matched_threshold:
                    return pred.to_list()

        # 如果 possibles 已经满足阈值要求, 则不继续匹配了. 意图匹配就是这么武断, 哈哈
        if pred.label:
            return pred.to_list()

        # 没办法, 只好彻底遍历.
        for label_hash in doc_map:
            doc_list = doc_map[label_hash]
            for doc in doc_list:
                s = doc.similarity(sentence_doc)
                if s >= threshold:
                    label = self.label_hash_map[label_hash]
                    pred = pred.append(label, s, limit)
        # 最终返回结果.
        return pred.to_list()
