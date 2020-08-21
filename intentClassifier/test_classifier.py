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

