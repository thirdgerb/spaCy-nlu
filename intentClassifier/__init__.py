
from .classifier import IntentClassifier


def create_classifier(
    nlu,
    matched_threshold=0.95
):
    return IntentClassifier(nlu, matched_threshold)


def init_classifier(
    matcher: IntentClassifier,
    example_dictionary: dict
):
    """
    初始化意图匹配
    :param matcher:
    :param example_dictionary:
    :return:
    """
    for label in example_dictionary:
        example_list = example_dictionary[label]
        matcher.learn_intent(label, example_list)
