import programstate
import textile
import os
import shutil
import sys

DEITY_PATH = "d8y"
DEF_BASEHTML_PATH = "basehtml"
DEF_REPLACE_PATH = "repl8ce"

DEF_INPUT = "input"
DEF_OUTPUT = "output"


def makedir(path, warning = ""):
    if not os.path.exists(path):
        if warning != "":
            print("WARNING: " + warning)
        os.mkdir(path)


# Genesis of a website
def genesis(name):
    if not name.isidentifier():
        raise Exception("Name must only contain alphanumeric letters (a-z and 0-9) or underscores (_). Cannot start with a number or contain spaces.")
    makedir(name)
    makedir(os.path.join(name, DEF_INPUT))
    makedir(os.path.join(name, DEF_OUTPUT))
    open(os.path.join(name, DEITY_PATH), 'a').close()
    open(os.path.join(name, DEF_BASEHTML_PATH), 'a').close()
    open(os.path.join(name, DEF_REPLACE_PATH), 'a').close()



# Divines a website
def divine():
    state = programstate.ProgramState()
    for subdir, dirs, files in os.walk(state.input_folder):
        for dir in dirs:
            path = os.path.join(subdir, dir).replace(state.input_folder, state.output_folder, 1)
            makedir(path)
            
        for file in files:
            path = os.path.join(subdir, file)
            outpath = path.replace(state.input_folder, state.output_folder, 1)
            outhtml = outpath.replace(".textile", ".html", -1)
            if path.endswith(".textile"):
                contents = ""
                with open(path, "r") as f:
                    file_split = f.read().split("-BEGINFILE-")
                    file_headers = ""
                    file_content = ""
                    if len(file_split) == 2:
                        file_headers = file_split[0]
                        file_content = file_split[1]
                    elif len(file_split) == 1:
                        file_headers = ""
                        file_content = file_split[0]
                    else:
                        raise Exception("More than one -BEGINFILE- markers")
                    contents = textile.textile(file_content)
                    contents = state.basehtml_content.replace("##CONTENT##", contents)
                    
                    filerepl = state.replacements.copy()
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
