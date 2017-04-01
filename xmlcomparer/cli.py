from xml.etree import ElementTree as ET  #TODO: Support lxml silently if installed
import click
from xmlcomparer import difftool


@click.command("compare")
@click.argument("file1")
@click.argument("file2")
#@click.option
def compare(file1, file2):
    """
    With no options, compares the files as they are, using the configured (external) diff tool
    """
    print("OK!")
    with open(file1):
        xml1 = ET.parse(file1)
    with open(file2):
        xml2 = ET.parse(file2)

    diff_file1 = file1
    diff_file2 = file2
    tool = difftool.DiffTool()
    #tool.diff_files(diff_file1, diff_file2)
    tool.diff_bytes(ET.tostring(xml1.getroot()), ET.tostring(xml2.getroot()))


if __name__ == "__main__":
    compare()
