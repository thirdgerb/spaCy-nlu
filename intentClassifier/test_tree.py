from .tree import Branch
from time import time_ns as ns
import unittest
import re


# 测试结果, 现在写的树性能上没有任何优势.
class TestTree(unittest.TestCase):
    def test_regex(self):
        a = "a.b.c.d_g-e"
        c = a.split(r'.')
        self.assertEqual(['a', 'b', 'c', 'd_g-e'], c)
        self.assertEqual(['a', 'b', 'c', 'd', 'g', 'e'], re.split(r'[.\-_]+', a))

    def test_append_branch(self):
        root = Branch('')
        path = ['a', 'b', 'c', 'd']
        path.reverse()
        branch = root.append_branch(path, 'hello')
        self.assertEqual(
            "hello",
            root.get_child('a').get_child('b').get_child('c').get_child('d').value
        )
        self.assertEqual("hello", branch.value)

    @staticmethod
    def make_44_elements():
        elements = []
        for i1 in range(1, 5):
            for i2 in range(1, 5):
                for i3 in range(1, 5):
                    for i4 in range(1, 5):
                        row = [i1, i2, i3, i4]
                        elements.append(row)
        return elements

    @staticmethod
    def make_44_tree():
        elements = TestTree.make_44_elements()
        root = Branch('')
        i = 0
        for el in elements:
            i += 1
            el.reverse()
            root.append_branch(el, str(i))
        return root

    def test_build_tree_by_self(self):
        root = TestTree.make_44_tree()
        # 总数
        self.assertEqual(list('1234'), list(root.children.keys()))
        count_num = 1 + 4 + 4 * 4 + 4 * 4 * 4 + 4 * 4 * 4 * 4
        self.assertEqual(count_num, root.count())
        leaves = root.all_leaves(True)
        self.assertEqual(256, len(leaves))

    def test_search_by_query_branch(self):
        root = TestTree.make_44_tree()
        searches = ['1234', '1243',  '2341',  '2444', '213*']
        query = Branch('')
        for search in searches:
            search_path = list(search)
            search_path.reverse()
            query.append_branch(search_path, search)

        query_leaves = query.all_leaves()

        self.assertEqual(5, len(query_leaves))
        self.assertTrue("1" in root.children)

        # 第一次生成缓存
        leaves = root.search_by_query_branch(query)
        leaves = root.search_by_query_branch(query)
        start = ns()
        leaves = root.search_by_query_branch(query)
        end = ns()
        gap = end - start
        self.assertEqual(4 + 4, len(leaves))

        elements = TestTree.make_44_elements()
        ele_strings = []
        for el in elements:
            string = ""
            for i in el:
                string += str(i)
            ele_strings.append(string)

        start = ns()
        matched = []
        for string in ele_strings:
            if string in searches:
                matched.append(string)
        end = ns()
        gap2 = end - start
        self.assertEqual(4, len(matched))
        print(gap2, gap)


if __name__ == '__main__':
    unittest.main()
