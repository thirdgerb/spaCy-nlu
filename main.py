import os
import json
import spacy
from sanic import Sanic
from sanic.response import json as s_json


def load_json(path: str):
    """
    读取 json 文件, 返回 dict
    :param string path:
    :return: dict
    """
    with open(path) as f:
        return json.load(f)


class IntentClassifier:
    doc_map = {}

    def __init__(self, spacy_nlp):
        self.nlp = spacy_nlp

    def read_from_dict(self, data: dict):
        for label in data:
            examples = data[label]
            for example in examples:
                self.learn(label, example)

    def learn(
        self,
        label: str,
        int_example: str
    ):
        if label not in self.doc_map:
            self.doc_map[label] = {}
        example_doc = self.nlp(int_example)
        self.doc_map[label][int_example] = example_doc

    def wrap(
        self,
        sentence: str
    ):
        return self.nlp(sentence)

    def predict(
        self,
        sentence_doc
    ):
        similarity = 0
        matched = ""
        for label in self.doc_map:
            example_map = self.doc_map[label]
            for example in example_map:
                example_doc = example_map[example]
                s = sentence_doc.similarity(example_doc)
                if s > similarity:
                    similarity = s
                    matched = label
                if s > 0.95:
                    break
        return {"likely": similarity, "label": matched}


# 读取配置
config_path = os.path.abspath("config.json")
config = load_json(config_path)

nlp = spacy.load(config["model"])
data_path = os.path.abspath("data.json")
intent_example_map = load_json(data_path)
# 完成 matcher 的初始化.
classifier = IntentClassifier(nlp)
classifier.read_from_dict(intent_example_map)

app = Sanic(config["name"])


@app.route("/")
async def index(request):
    sentence_doc = classifier.wrap("hello world")
    prediction = classifier.predict(sentence_doc)
    return s_json({"test": prediction})


@app.route('/learn', methods=['POST'])
async def learn(request):
    req_data = request.json
    label = req_data["label"]
    sentence = req_data["sentence"]
    if not label or not sentence:
        return s_json({"code": 400, "msg": "invalid request"})
    classifier.learn(label, sentence)
    return s_json({"code": 0, "msg": "success"})


@app.route('/predict', methods=['GET'])
async def predict(request):
    req_data = request.json
    sentence = req_data["sentence"]
    if not sentence:
        return s_json({"code": 400, "msg": "invalid request"})
    sentence_doc = classifier.wrap(sentence)
    prediction = classifier.predict(sentence_doc)
    return s_json({"code": 0, "msg": "success", "data": prediction})


if __name__ == "__main__":
    debug = config["debug"] == "true"
    app.run(host=config["host"], port=config["port"], debug=False, access_log=False)
