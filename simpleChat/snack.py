class ChatNode:
    doc = None
    reply = ""

    def __init__(self, doc, reply: str):
        self.doc = doc
        self.reply = reply


class ChatSnack:
    matched = []
    awaits = []

    def __init__(self, doc, reply: str):
        self.append(doc, reply)

    def append(self, doc, reply: str):
        node = ChatNode(doc, reply)
        # 新来的总在前面
        self.awaits.insert(0, node)

    def set_matched(self, node: ChatNode):
        # 暂时用最简单的办法, 让命中过的放最前面.
        i = self.awaits.index(node)
        self.matched.insert(0, node)
        del self.awaits[i]

    def reply(
        self,
        doc,
        threshold=0.95
    ):
        similarity = 0.0
        matched = None
        for current in self.matched:
            s = current.doc.similarity(doc)
            if s >= threshold:
                return current.reply, s
            if s > similarity:
                matched = current

        for current in self.awaits:
            s = current.doc.similarity(doc)
            if s >= threshold:
                self.set_matched(current)
                return current.reply, s
            if s > similarity:
                matched = current
        if matched:
            return matched.reply, similarity
        else:
            return "", 0.0

# 弃用了!  这种做法还是更新数据太频繁, 对性能没信心
#
# class ChatNode:
#     prev = None
#     next = None
#     doc = None
#     reply = ""
#     id = 0
#
#     def __init__(self, doc, reply: str, snack_id: int):
#         self.doc = doc
#         self.reply = reply
#         self.id = snack_id
#
#
# class ChatSnack:
#     head = None
#     tail = None
#     ind = 0
#     body = {}
#
#     def __init__(self, doc, reply: str):
#         initial_node = ChatNode(doc, reply, self.ind)
#         self.head = initial_node
#         self.tail = initial_node
#         self.body[initial_node.id] = initial_node
#
#     def append(self, doc, reply: str):
#         self.ind = self.ind + 1
#         node = ChatNode(doc, reply, self.ind)
#
#         node.prev = self.tail
#         self.tail.next = node
#         # head 不变
#         self.tail = node
#
#     def set_matched(self, node: ChatNode):
#         """
#         换头大法!
#         :param node:
#         :return:
#         """
#
#         # 自己就是头, 换个鬼, 会死循环的.
#         if self.head.id == node.id:
#             return
#
#         elder = node.prev
#         younger = node.next
#         # 缝合兄弟姐妹
#         if elder:
#             elder.next = younger
#         if younger:
#             younger.prev = elder
#         # 没有弟妹说明自己是尾巴, 换尾巴
#         else:
#             self.tail = elder
#
#         # 新旧头缝在一起
#         node.prev = None
#         node.next = self.head
#         self.head.prev = node
#         self.head = node
