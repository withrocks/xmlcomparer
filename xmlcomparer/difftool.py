import subprocess
import tempfile


class DiffTool(object):
    """Handles communication with an external diff tool"""
    def __init__(self):
        # TODO: Figure out which tool to use using different rules:
        #  * config (env variables)
        #  * git if installed?

        # Uses the same syntax as in the config for git:
        self.external_cmd = "vimdiff $LOCAL $REMOTE"

    def diff_files(self, path_a, path_b):
        cmd = self.external_cmd.replace("$LOCAL", path_a)
        cmd = cmd.replace("$REMOTE", path_b)
        # TODO: Wouldn't support quotation marks in the cmd
        subprocess.call(cmd.split(" "))

    def diff_bytes(self, bstr1, bstr2):
        """First writes the strings to temporary files, then compares the files"""
        print(bstr1.decode())
        print(bstr2.decode())
        return
        file1 = tempfile.NamedTemporaryFile()
        file1.write(bstr1)
        file1.flush()
        file2 = tempfile.NamedTemporaryFile()
        file2.write(bstr2)
        file2.flush()
        self.diff_files(file1.name, file2.name)
        file1.close()
        file2.close()
