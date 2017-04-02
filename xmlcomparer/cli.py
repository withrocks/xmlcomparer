from xml.etree import ElementTree as ET  #TODO: Support lxml silently if installed
import click
from xmlcomparer import difftool
from xmlcomparer import transformer


@click.command("compare")
@click.argument("file1")
@click.argument("file2")
@click.option("--ignore-order/--no-ignore-order")
def compare(file1, file2, ignore_order):
    """
    With no options, compares the files as they are, using the configured (external) diff tool
    """
    import logging
    logging.basicConfig(level=logging.DEBUG)
    with open(file1):
        xml1 = ET.parse(file1)
    with open(file2):
        xml2 = ET.parse(file2)

    diff_file1 = file1
    diff_file2 = file2
    tool = difftool.DiffTool()
    t = transformer.Transformer(xml1)
    # Apply an action in a scope, here we ignore the order for any element:
    t.ignore_order(".*")

    # 1. apply selectors and actions:
    #t.transform()

    print("---")
    t2 = transformer.Transformer(xml2)
    t2.ignore_order(".*")
    t2.transform()

    # 2. Then diff
    #tool.diff_bytes(ET.tostring(xml1.getroot()), ET.tostring(xml2.getroot()))

if __name__ == "__main__":
    compare()
