import os

def makedir(path, warning = ""):
    if not os.path.exists(path):
        if warning != "":
            print("WARNING: " + warning)
        os.mkdir(path)


class ProgramState:
    deity_path = "d8y"
    def __init__(self):
        self.deity_path = "d8y"
        self.basehtml_path = "basehtml"
        self.replacements_path = "repl8ce"
        self.replacements = {}

        self.input_folder = "input"
        self.output_folder = "output"
        
        if not os.path.exists(self.deity_path):
            raise Exception("No " + self.deity_path + " file found")
        
        # Core Renaming
        with open(self.deity_path, "r") as d8y_file:
            for line in d8y_file.readlines():
                keyval = line.split("=")
                if len(keyval) != 2:
                    raise Exception("Error in d8y file format:\n   " + line)
                if keyval[0] == "input" and keyval[1].isidentifier():
                    self.input_folder = keyval[1]
                elif keyval[0] == "output" and keyval[1].isidentifier():
                    self.output_folder = keyval[1]
                elif keyval[0] == "replace" and keyval[1].isidentifier():
                    self.replacements_path = keyval[1]
                elif keyval[0] == "basehtml" and keyval[1].isidentifier():
                    self.basehtml_path = keyval[1]

        if not os.path.exists(self.basehtml_path):
            raise Exception("No" + self.basehtml_path + "file found")

        self.basehtml_content = open(self.basehtml_path, "r").read()


        makedir(self.input_folder, "No input directory found, creating one")
        makedir(self.output_folder, "No output directory found, creating one")

        # Load the replacements from repl8ce
        if os.path.exists(self.replacements_path):
            replacement_text = open(self.replacements_path, "r").readlines()
            for i in replacement_text:
                if replacement_text != "":
                    rep_key = i.split("=")
                    if len(rep_key) == 2:
                        self.replacements[rep_key[0]] = rep_key[1]
                    elif len(rep_key) == 1:
                        self.replacements[rep_key[0]] = ""
                    else:
                        raise Exception("More than one value assignments on a replace key")
        else:
            print("WARNING: No " + self.replacements_path + " file found, continuing")