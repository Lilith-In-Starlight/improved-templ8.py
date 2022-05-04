import textile
import os
import shutil
import sys

deity_path = "d8y"
basehtml_path = "basehtml"
replacements_path = "rpl8cmnt"

replacements = {}

input_folder = "input"
output_folder = "output"


def makedir(path, warning = ""):
    if not os.path.exists(path):
        if warning != "":
            print("WARNING: " + path)
        os.mkdir(path)


# Genesis of a website
def genesis(name):
    if not name.isidentifier():
        raise Exception("Name must only contain alphanumeric letters (a-z and 0-9) or underscores (_). Cannot start with a number or contain spaces.")
    makedir(name)
    makedir(os.path.join(name, input_folder))
    makedir(os.path.join(name, output_folder))
    open(os.path.join(name, deity_path), 'a').close()
    open(os.path.join(name, basehtml_path), 'a').close()
    open(os.path.join(name, replacements_path), 'a').close()


# Updates the variables
def load_project():
    if not os.path.exists(deity_path):
        raise Exception("No " + deity_path + " file found")

    if not os.path.exists(basehtml_path):
        raise Exception("No" + basehtml_path + "file found")

    basehtml_content = open(basehtml_path, "r").read()


    makedir(input_folder, "No input directory found, creating one")
    makedir(output_folder, "No output directory found, creating one")

    # Load the replacements from rpl8cmnt
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
        print("WARNING: No" + repl8cmnt + "file found, continuing")

# Divines a website
def divine():
    load_project()
    for subdir, dirs, files in os.walk(input_folder):
        for dir in dirs:
            path = os.path.join(subdir, dir).replace(input_folder, output_folder, 1)
            makedir(path)
            
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


def help(cmd = ""):
    if cmd == "":
        print("""
        
    ###                                                                 
    ###                                                               ###
    ###                                                               ###       #####
###########        ###                                                ###     ##    ###
###########     #########      ### ####    #####      ### ######      ###    ##      ###
    ###        ###     ###     ###################    ############    ###    ##     ####
    ###       ###       ###    ###    ####    ####    ###      ####   ###     ##   ####
    ###       #############    ###     ###     ###    ###       ###   ###      #######
    ###       #############    ###     ###     ###    ###      ####   ###    ####    ##
  #######     ###              ###     ###     ###    ############    ###   ####       ##
    ###       ####      ###    ###     ###     ###    ##########      ###   ###        ##
    ###         ##########     ###     ###     ###    ###             ###    ###     ###
    ##            ######       ###     ###     ###    ###             ###      ####### 
    ##                                                ###
    #

help        Display this list.
genesis     Create a new templ8 page.
divine      Build a templ8 page.
""")                                            

if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) == 1:
        help()
    elif len(sys.argv) == 2:
        if sys.argv[1] == "help":
            help()
        elif sys.argv[1] == "divine":
            divine()
    elif len(sys.argv) == 3:
        if sys.argv[1] == "genesis":
            genesis(sys.argv[2])
        else:
            raise Exception("Unexpected number of arguments")
