# coding=utf-8
import os
import json
import spacy
from sanic import Sanic
from sanic.response import json as s_json
from intentClassifier import create_classifier, init_classifier
from simpleChat import create_simple_chat


def load_json(path: str):
    """
    读取 json 文件, 返回 dict
    :param string path:
    :return: dict
    """
    with open(path) as f:
        return json.load(f)


# 读取配置
config_path = os.path.abspath("config.json")
config = load_json(config_path)

# 初始化 nlp
nlp = spacy.load(config["model"])
# 完成 matcher 的初始化.
data_path = os.path.abspath("intents.json")
intent_example_map = load_json(data_path)
classifier = create_classifier(nlp)
init_classifier(classifier, intent_example_map)

# 初始化 chat
chat = create_simple_chat(nlp)

# 开始初始化 app
app = Sanic(config["name"])


@app.route("/")
async def index(request):
    sentence_doc = classifier.nlp("hello world")
    prediction = classifier.predict(sentence_doc)
    return s_json({"test": prediction})


@app.route('/classifier/learn', methods=['POST'])
async def learn(request):
    req_data = request.json
    label = req_data["label"]
    sentence = req_data["sentence"]
    if not label or not sentence:
        return s_json({"code": 400, "msg": "invalid request"})
    classifier.learn(label, sentence)
    return s_json({"code": 0, "msg": "success"})


@app.route('/classifier/predict', methods=['GET'])
async def predict(request):
    req_data = request.json
    sentence = req_data["sentence"]
    possibles = req_data["possibles"] or []
    threshold = req_data["threshold"] or 0.8
    limit = req_data["limit"] or 5

    if not sentence:
        return s_json({"code": 400, "msg": "invalid request"})
    sentence_doc = classifier.nlp(sentence)
    prediction = classifier.predict(sentence_doc, possibles, threshold, limit)
    return s_json({"code": 0, "msg": "success", "classification": prediction})


if __name__ == "__main__":
    debug = config["debug"] == "true"
    app.run(host=config["host"], port=config["port"], debug=False, access_log=False)
