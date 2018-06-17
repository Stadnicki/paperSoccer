import os


class ResultsFile:
    def __init__(self, file_name):
        self.file_name = file_name

    def add_result(self, content):
        with open(self.file_name, "a+") as f:
            f.write(content+'\n\n')
            f.close()

    def get_result(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, "r") as f:
                return f.read()
        else:
            open(self.file_name, "w")
            return ''

