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
classifier = create_classifier(nlp, config["classifier_matched_threshold"])

intent_data_file = os.path.abspath("intents.json")
if os.path.exists(intent_data_file):
    intent_example_map = load_json(intent_data_file)
    init_classifier(classifier, intent_example_map)
    print("load intent data:" + intent_data_file)

# 初始化 chat
chat = create_simple_chat(nlp, config["chat_matched_threshold"])
chat_data_file = os.path.abspath("chats.json")
if os.path.exists(chat_data_file):
    chat_data_list = load_json(chat_data_file)
    for index in chat_data_list:
        for chat_data in chat_data_list[index]:
            chat.learn(chat_data["cid"], chat_data["say"], chat_data["reply"], index)
    print("load chat data:" + chat_data_file)

# 开始初始化 app
app = Sanic(config["name"])


@app.route("/")
async def index(request):
    sentence_doc = classifier.nlp("hello world")
    prediction = classifier.predict(sentence_doc, [], 0.75, 5)
    return s_json({"test": prediction})


@app.route('/classifier/learn', methods=['POST'])
async def classifier_learn(request):
    req_data = request.json
    if "label" not in req_data \
            or not req_data["label"] \
            or "sentence" not in req_data \
            or not req_data["sentence"]:
        return s_json({"code": 400, "msg": "invalid request"})

    label = req_data["label"]
    sentence = req_data["sentence"]
    classifier.learn(label, sentence)
    return s_json({"code": 0, "msg": "success"})


@app.route('/classifier/learn-intent', methods=['POST'])
async def classifier_learn_intent(request):
    req_data = request.json
    if "label" not in req_data \
            or "examples" not in req_data \
            or not (type(req_data["examples"]) == list):
        return s_json({"code": 400, "msg": "invalid request"})

    label = req_data["label"]
    examples = req_data["examples"]
    classifier.learn_intent(label, examples)
    return s_json({"code": 0, "msg": "success"})


@app.route('/classifier/predict', methods=['GET'])
async def classifier_predict(request):
    req_data = request.json

    if "sentence" not in req_data \
            or type(req_data["sentence"]) != str \
            or "possibles" not in req_data \
            or type(req_data["possibles"]) != list \
            or "threshold" not in req_data \
            or type(req_data["threshold"]) != float \
            or "limit" not in req_data \
            or type(req_data["limit"]) != int:
        return s_json({"code": 400, "msg": "invalid request"})

    sentence = req_data["sentence"]
    possibles = req_data["possibles"]
    threshold = req_data["threshold"]
    limit = req_data["limit"]

    sentence_doc = classifier.nlp(sentence)
    prediction = classifier.predict(sentence_doc, possibles, threshold, limit)
    return s_json({"code": 0, "msg": "success", "proto": prediction})


@app.route('/chat/learn', methods=['POST'])
async def chat_learn(request):
    req_data = request.json
    if "cid" not in req_data \
            or type(req_data["cid"]) != str \
            or "say" not in req_data \
            or type(req_data["say"]) != str \
            or "reply" not in req_data \
            or type(req_data["reply"]) != str \
            or "index" not in req_data \
            or type(req_data["index"]) != str:
        return s_json({"code": 400, "msg": "invalid request"})

    cid = req_data["cid"]
    say = req_data["say"]
    reply = req_data["reply"]
    chat_index = req_data["index"]
    if not cid or not say or not reply:
        return s_json({"code": 400, "msg": "invalid request"})

    chat.learn(cid, say, reply, chat_index)
    return s_json({"code": 0, "msg": "success"})


@app.route('/chat/reply', methods=['GET'])
async def chat_reply(request):
    req_data = request.json

    if "index" not in req_data \
            or type(req_data["index"]) != str \
            or "say" not in req_data \
            or type(req_data["say"]) != str \
            or "threshold" not in req_data \
            or type(req_data["threshold"]) != float:
        return s_json({"code": 400, "msg": "invalid request"})

    chat_index = req_data["index"]
    threshold = req_data["threshold"]
    say = req_data["say"]

    r = chat.reply(say, threshold, chat_index)
    return s_json({"code": 0, "msg": "success", "proto": r})


if __name__ == "__main__":
    debug = config["debug"]
    access_log = config["access_log"]
    app.run(host=config["host"], port=config["port"], debug=debug, access_log=access_log)
