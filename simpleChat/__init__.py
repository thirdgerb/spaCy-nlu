
from .simpleChat import SimpleChat


def create_simple_chat(nlp, matched_threshold=0.95):
    return SimpleChat(nlp, matched_threshold)


def init_simple_chat(chat: SimpleChat, data_list: list):
    for chat_info in data_list:
        chat.learn(chat_info["cid"], chat_info["say"], chat_info["reply"])

