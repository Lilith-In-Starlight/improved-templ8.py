import textile
import os
import shutil
import warnings

deity_path = "d8ty"
basehtml_path = "basehtml"
replacements_path = "rpl8cmnt"

replacements = {}

input_folder = "input"
output_folder = "output"


if not os.path.exists(deity_path):
    raise Exception("No d8ty file found")

if not os.path.exists(basehtml_path):
    raise Exception("No basehtml file found")

basehtml_content = open(basehtml_path, "r").f.read()


if not os.path.exists(input_folder):
    warnings.warn("No input directory found, creating one")
    os.mkdir(input_folder)
if not os.path.exists(output_folder):
    warnings.warn("No output directory found, creating one")
    os.mkdir(input_folder)

if os.path.exists(replacements_path):
    replacement_text = open(replacements_path, "r").readlines()
    for i in replacement_text:
        if replacement_text != "":
            rep_key = i.split("=")
            if len(rep_key) == 2:
                replacements[rep_key[0]] = rep_key[1]
            elif len(rep_key) == 1:
                replacements[rep_key[0]] = ""
            else:
                raise Exception("More than one value assignments on a replace key")
else:
    warnings.warn("No rpl8cmnt file found, continuing")


for subdir, dirs, files in os.walk(input_folder):
    for dir in dirs:
        path = os.path.join(subdir, dir)
        if not os.path.exists(path):
            os.mkdir(path.replace(input_folder, output_folder, 1))
    
    for file in files:
        path = os.path.join(subdir, file)
        outpath = path.replace(input_folder, output_folder, 1)
        outhtml = outpath.replace(".textile", ".html", -1)
        if path.endswith(".textile"):
            contents = ""
            with open(path, "r") as f:
                file_split = f.read().split("-BEGINFILE-")
                if len(file_split) == 2:
                    file_headers = file_split[0]
                    file_content = file_split[1]
                elif len(file_split) == 1:
                    file_headers = ""
                    file_content = file_split[0]
                else:
                    raise Exception("More than one -BEGINFILE- markers")
                contents = textile.textile(file_content)
                contents = basehtml_content.replace("##CONTENT##", contents)
                
                filerepl = replacements.copy()
                for replace in file_headers.split("\n"):
                    if replace != "":
                        keyval = replace.split("=")
                        filerepl[keyval[0]] = keyval[1]
                
                for key in filerepl:
                    contents = contents.replace("##"+key+"##", filerepl[key])
                
                
               
            with open(outhtml, "w") as f:
                f.write(contents)
                
        elif not os.path.exists(outpath):
            shutil.copy(path, outpath)

print("Finished assembling")