import os
from unittest import TestCase
from intentClassifier.classifier import IntentClassifier
import spacy
import json
import time

nlp = spacy.load("zh_core_web_md")


class TestClassifier(TestCase):
    def test_predict(self):
        classifier = IntentClassifier(nlp, 0.95)
        path = os.path.abspath("intentClassifier/stub.json")
        with open(path) as f:
            json_data = json.load(f)

        for intent in json_data:
            examples = json_data[intent]
            classifier.learn_intent(intent, examples)

        for intent in json_data:
            examples = json_data[intent]
            for exp in examples:
                exp_doc = classifier.nlp(exp)
                output = classifier.predict(exp_doc, [intent])
                self.assertEqual(intent, output[0]["label"])
                self.assertTrue(output[0]["similarity"] > 0.95)

    def test_learn_intent(self):
        classifier = IntentClassifier(nlp, 0.95)
        classifier.learn_intent('test', ['test abc', 'test efg', 'test more'])
        doc = classifier.nlp('test abc')
        matched = classifier.predict(doc, [])
        self.assertEqual('test', matched[0]["label"])
        classifier.learn_intent('test', ['hello', 'hello world'])

        matched = classifier.predict(doc, [])
        self.assertEqual(0, len(matched))
        search2 = 'hello world'
        search2_doc = classifier.nlp(search2)
        matched = classifier.predict(search2_doc, [])
        self.assertEqual('test', matched[0]["label"])

    def test_learn_special_case(self):
        classifier = IntentClassifier(nlp, 0.95)
        intent = 'navigation.bot.wrong'
        classifier.learn_intent(intent, ['答非所问', '胡说八道', '你胡扯些什么', '前言不搭后语', '完全理解错了', '你没有理解我的意思'])
        test_doc = classifier.nlp('胡说八道')
        prediction = classifier.predict(test_doc, [])
        self.assertEqual(intent, prediction[0]["label"])



