from unittest import TestCase
from .simpleChat import SimpleChat
import spacy

nlp = spacy.load("zh_core_web_md")

text = """我从山中来
带着兰花草
家中无富贵
口袋无财宝
寒风终刺骨
勤为好仕途
博得明月出
用兰花换锦服
走的那天飘起了小雨
为了赶路我选择早起
山间里飘起了雾
路过有诗仙的墓
给我指方向在哪里
一路上有花香和鸟语
带上兄弟给我做的好beat
看我用808打底
再把裤子要跨起
背上是山城烙印
下山去 下山去
林间小道做标记
用心听 用力取
挥手告别好兄弟
地为床 天为铺
少侠莫怕草木枯
日为钟 月为弓
勿忘茅屋有寒冬
宝骏 踏断 命里刺
胭脂 洒满 暮光谷
他日 若随 凌云志
敢笑 黄巢 不丈夫
冲动了我 耽误了我
一扇门关闭了 拴上了锁
钢做绞索 你关不到我
一把火点燃了 干柴草垛
青莲居士点了我的脑壳
我跟他说没得东西好学
生老病死不再需要草药
七情六欲赐给我的宝座
除非黑白亲自唤
秦广自来勾
九灵归于兰花草
一魄丧冥幽
我盼的是梁园月
渴的是东京酒
等的是洛阳花
撰的是章台柳
"""


class TestSimpleChat(TestCase):
    def test_reply(self):
        chat = SimpleChat(nlp)
        lines = text.split("\n")
        current = None
        for line in lines:
            last = current
            current = line
            if last and current:
                chat.learn(last, current)

        for line in lines:
            last = current
            current = line
            if last and current:
                result = chat.reply(last, 0.85)
                self.assertEqual(current, result["reply"])





