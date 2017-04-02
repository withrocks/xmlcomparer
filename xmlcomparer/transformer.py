import copy
import logging
from xml.etree import ElementTree as ET

logger = logging.getLogger(__name__)


class ElementIterator(object):
    def __init__(self, element):
        self.element = element
        self.ignore_order = False

    def __iter__(self):
        # NOTE: Reordering will have an effect on the tail (whitespace following elements)
        # Here we'll use the trick of replacing tail based on ordering. (Another trick would be
        # to just pretty-print the entire file when done transforming.)
        if self.ignore_order:
            # As-is this must be materialized, as we will be modifying the elements in the loop
            tails = [e.tail for e in self.element]
            for child, orig_tail in zip(sorted(self.element, key=lambda e: e.tag), tails):
                child.tail = orig_tail
                yield child
        else:
            for child in self.element:
                yield child


class Transformer(object):
    """
    Transforms the original object

    NOTE: This is a POC, performance is almost completely ignored
    """
    RULE_IGNORE_ORDER = 1

    def __init__(self, original):
        self.original = original
        # TODO: Create only if required
        self.transformed = copy.deepcopy(original)
        self.rules = list()

    def apply_action(self, element, iterator, path, action):
        logger.debug("Applying action {} to element {}".format(action, element))
        if action == self.RULE_IGNORE_ORDER:
            iterator.ignore_order = True

    def transform_element(self, element, path):
        # NOTE: whitespaces not preserved
        transformed_element = ET.Element(element.tag, attrib=element.attrib)
        transformed_element.text = element.text
        transformed_element.tail = element.tail  # I.e. whitespace following the tag
        path = "{}{}/".format(path, element.tag)
        logger.debug("Transforming element '{}' at '{}' (=> {})".format(element.tag, path, transformed_element))
        logger.debug(" - Original element text: '{}'".format(element.text))
        iterator = ElementIterator(element)
        # Check what selectors apply for this element:
        for rule, action in self.rules:
            if rule.match(path):
                self.apply_action(element, iterator, path, action)

        for child in iterator:
            new_child = self.transform_element(child, path)
            transformed_element.append(new_child)
        return transformed_element

    def transform(self):
        # Walk the tree and, for each row, check if we
        element = self.transformed.getroot()
        transformed_root = self.transform_element(element, "/")
        transformed_doc = ET.ElementTree(transformed_root)
        return transformed_doc

    def ignore_tag_order(self, element_selector):
        """
        Given a selector, ignores the order of all child elements.

        The selector can be a regular expression that will be applied to the path
        of the element. NOTE: This might be replaced with xpath later.

        So if you have this XML
        <root>
          <a><b/></a>
          <c/>
        </root>

        You can select the b element with the selector /root/.*/b
        """
        import re
        rule = re.compile(element_selector)
        self.rules.append((rule, self.RULE_IGNORE_ORDER))

