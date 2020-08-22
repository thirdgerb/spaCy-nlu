import re


class Branch:

    def __init__(self, bid):
        self.bid = str(bid)
        self.children = {}
        self.value = None
        self._all_leaves = None

    @staticmethod
    def build_tree_by_list(leaves: list):
        root = Branch("")
        for string in leaves:
            branch_path = re.split(r'[.\-_]+', string)
            branch_path.reverse()
            root.append_branch(branch_path, string)
        return root

    # 长出新枝.
    def append_branch(self, branch_path: list, value):
        if len(branch_path) > 0:
            node = branch_path.pop()
            node = str(node)
            if node not in self.children:
                self.children[node] = Branch(node)
            return self.children[node].append_branch(branch_path, value)
        else:
            self.value = value
            return self

    def get_child(self, child):
        return self.children[child]

    # 是否有孩子
    def has_child(self):
        return len(self.children) > 0

    # 叶子节点
    def is_leaf(self):
        return self.value is not None

    # 返回所有的叶子节点
    def all_leaves(self, with_self=False):
        if self._all_leaves is None:
            leaves = []
            if with_self and self.is_leaf():
                leaves.append(self)
            for child in self.children:
                child_leaves = self.children[child].all_leaves(True)
                leaves.extend(child_leaves)
            self._all_leaves = leaves
        return self._all_leaves

    def all_leaves_without(self, with_out: list, with_self=False):
        leaves = []
        if with_self and self.is_leaf():
            leaves.append(self)
        children = self.children.keys()
        children = list(set(children).difference(set(with_out)))
        for child in children:
            child_branch = self.children[child]
            child_leaves = child_branch.all_leaves(True)
            leaves.extend(child_leaves)
        return leaves

    def search_leaf(self, leaf_path: list):
        """
        寻找一片叶子.
        :param leaf_path:
        :return:
        """
        length = len(leaf_path)
        if length == 0:
            if self.is_leaf():
                return self
            else:
                return None
        node = leaf_path.pop()
        if node in self.children:
            child = self.children[node]
            return child.search_leaf(leaf_path)
        else:
            return None

    def count(self):
        c = 1
        for child in self.children:
            c += self.children[child].count()
        return c

    # 用另一个多枝杈的树来查找叶子.
    # 只有用 * 在结尾做通配符时才能批量匹配
    def search_by_query_branch(self, query_branch):
        self_is_leaf = self.is_leaf()
        # 没有子节点了, query 到头了, 查到的就是当前节点
        if query_branch.has_child() is False:
            if self_is_leaf:
                return [self]
            else:
                return []

        # 自己没有子节点了, 说明 query 错了.
        if self.has_child() is False:
            return []

        found_leaves = []
        # 否则就儿子找儿子.
        search_all = False
        queries = query_branch.children.copy()
        if "*" in queries:
            wild_match = query_branch.children["*"]
            if wild_match.has_child() is False:
                # 通配符只能在结尾, 不能在中间. 否则就变成 m * n 的正则匹配了.
                search_all = True
            del queries["*"]

        searched_children = []
        for child in queries:
            length = len(child)
            last = length - 1
            # 如果以有 child 名, 并且以 * 结尾, 表示通配包括它在内的所有子节点.
            if child[last] == '*':
                child = child[0:last-1]
                if child in self.children:
                    child_branch = self.children[child]
                    child_searched = child_branch.all_leaves(with_self=True)
                    found_leaves.extend(child_searched)
                    searched_children.append(child)
                continue

            # 逐个子节点搜索.
            if child in self.children:
                child_query = queries[child]
                child_branch = self.children[child]
                child_searched = child_branch.search_by_query_branch(child_query)
                found_leaves.extend(child_searched)
                searched_children.append(child)
                continue

        # 确定要寻找所有子节点的话
        if search_all:
            all_leaves = self.all_leaves_without(searched_children, with_self=False)
            found_leaves.extend(all_leaves)
        return found_leaves






















