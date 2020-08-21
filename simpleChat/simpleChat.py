from .snack import ChatSnack


class SimpleChat:
    nlp = None
    # 让匹配过的自然在前面. 尽量不要频繁更动数据结构.
    snack = None

    def __init__(
        self,
        nlp
    ):
        self.nlp = nlp

    def learn(
        self,
        say: str,
        reply: str
    ):
        if not say or not reply:
            return
        doc = self.nlp(say)
        if not doc.has_vector:
            return

        if self.snack:
            self.snack.append(doc, reply)
        else:
            self.snack = ChatSnack(doc, reply)

    def reply(
        self,
        say: str,
        matched_threshold=0.95
    ):
        if not say:
            return self.empty_reply()

        if not self.snack:
            return self.empty_reply()

        say_doc = self.nlp(say)
        result = self.snack.reply(say_doc, matched_threshold)
        return {"reply": result[0], "likely": result[1]}

    @staticmethod
    def empty_reply():
        return {"reply": "", "likely": 0.0}
