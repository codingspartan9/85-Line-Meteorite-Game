import os


class FileReader:
    name_to_data = {}

    def __init__(self, file_path):
        lines = self.get_lines(file_path)
        for line in lines:
            delimiter_start = line.index(":")
            name = line[:delimiter_start]
            data = line[delimiter_start + 1:]

            self.name_to_data[name] = data

    def get_lines(self, file_path):
        current_line = ""
        enter = """
"""
        lines = []
        file = open(os.getcwd() + "\\" + file_path, "r+")

        for ch in file.read():
            if ch == enter:
                lines.append(current_line)
                current_line = ""

            else:
                current_line += ch

        if current_line != "":
            lines.append(current_line)

        file.close()
        return lines

    def get_int(self, name):
        return int(self.name_to_data[name])

    def get_float(self, name):
        return float(self.name_to_data[name])

    def get_boolean(self, name):
        return self.name_to_data[name] == "True"

    def get_string_list(self, name):
        string_list = []
        current_item = ""

        data = self.name_to_data[name]

        for ch in data[1:-1]:
            if ch == ",":
                string_list.append(current_item)
                current_item = ""

            else:
                current_item += ch

        if current_item != "":
            string_list.append(current_item)

        return string_list

    def get_float_list(self, name):
        string_list = self.get_string_list(name)
        float_list = []

        for item in string_list:
            float_list.append(float(item))

        return float_list

