
class ChatNode:

    def __init__(self, cid: str, origin: str, doc, reply: str):
        self.cid = cid
        self.origin = origin
        self.doc = doc
        self.reply = reply


class ChatGroup:

    def __init__(self, matched_threshold=0.85):
        self.matched_threshold = matched_threshold
        self.awaits = {}
        self.matched = {}
        self.matched_threshold = 0.85

    def add(self, cid: str, origin: str, doc, reply: str):
        node = ChatNode(cid, origin, doc, reply)
        cid_hash = hash(cid)
        # 新来的总在前面
        if cid_hash in self.matched:
            self.matched[cid_hash] = node
        else:
            self.awaits[cid_hash] = node

    def set_matched(self, node: ChatNode):
        # 暂时用最简单的办法, 让命中过的放最前面.
        cid_hash = hash(node.cid)
        del self.awaits[cid_hash]
        self.matched[cid_hash] = node

    def reply(
        self,
        doc,
        threshold=0.85
    ):
        similarity = 0.0
        matched = None
        matched_threshold = self.matched_threshold
        matched_map = self.matched

        for id_hash in matched_map:
            current = matched_map[id_hash]
            s = current.doc.similarity(doc)
            if s >= matched_threshold:
                return current.origin, current.reply, s
            if s > threshold and s > similarity:
                similarity = s
                matched = current

        awaits_map = self.awaits
        for id_hash in awaits_map:
            current = awaits_map[id_hash]
            s = current.doc.similarity(doc)
            if s >= matched_threshold:
                self.set_matched(current)
                return current.origin, current.reply, s
            if s > threshold and s > similarity:
                similarity = s
                matched = current

        if matched:
            return matched.origin, matched.reply, similarity
        else:
            return "", "", 0.0

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
