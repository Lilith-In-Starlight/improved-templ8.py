import os

def makedir(path, warning = ""):
    if not os.path.exists(path):
        if warning != "":
            print("WARNING: " + path)
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