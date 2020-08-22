from .group import ChatGroup


class SimpleChat:

    DEFAULT_INDEX = 'default'

    def __init__(
        self,
        nlp,
        matched_threshold=0.95
    ):
        self.nlp = nlp
        self.chats = {}
        self.matched_threshold = matched_threshold

    def learn(
        self,
        cid: str,
        say: str,
        reply: str,
        index=''
    ):
        if not cid or not say or not reply:
            return

        doc = self.nlp(say)
        if not doc.has_vector:
            return

        index = index or self.DEFAULT_INDEX
        if index not in self.chats:
            self.chats[index] = ChatGroup(self.matched_threshold)
        group = self.chats[index]
        group.add(cid, say, doc, reply)

    def reply(
        self,
        say: str,
        threshold=0.85,
        index=''
    ):
        index = index or self.DEFAULT_INDEX
        if not say:
            return self.empty_reply()

        if index not in self.chats:
            return self.empty_reply()

        chat = self.chats[index]
        say_doc = self.nlp(say)
        result = chat.reply(say_doc, threshold)
        return {"matched": result[0], "reply": result[1], "likely": result[2]}

    @staticmethod
    def empty_reply():
        return {"matched": "", "reply": "", "likely": 0.0}
