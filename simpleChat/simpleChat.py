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
        say: str,
        reply: str,
        index=''
    ):
        if not say or not reply:
            return

        doc = self.nlp(say)
        if not doc.has_vector:
            return

        index = index or self.DEFAULT_INDEX
        if index not in self.chats:
            self.chats[index] = ChatGroup(self.matched_threshold)
        group = self.chats[index]
        group.append(doc, reply)

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
        return {"reply": result[0], "likely": result[1]}

    @staticmethod
    def empty_reply():
        return {"reply": "", "likely": 0.0}
