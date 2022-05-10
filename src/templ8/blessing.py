import os
import textile
import pypandoc

TEMPL8_ASCII = """
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
    #"""
DEF_BASEHTML_CONTENT = """PAGETITLE=##TITLE##
-BEGINFILE-
h2. ##TITLE##

^##AUTHORS## - ##TAGS## - ##DATE##^

##CONTENT##

-BEGININDEX-
h2. "##TITLE##":##LINK##

^##AUTHORS## - ##TAGS## - ##DATE##^

##INTRO##
-BEGININDEX-
PAGETITLE=Blog"""

DEF_INPUT = "input"
DEF_OUTPUT = "output"
DEITY_PATH = "d8y"
DEF_BASEHTML_PATH = "basehtml"
DEF_REPLACE_PATH = "repl8ce"

def makedir(path, warning = ""):
    if not os.path.exists(path):
        if warning != "":
            print("WARNING: " + warning)
        os.mkdir(path)


def mod_replaces(input_replaces, header):
    current_multival = ""
    current_multikey = ""
    multiline = False
    for i in header.split("\n"):
        keyval = i.split("=", 1)
        if len(keyval) == 2 and not multiline:
            input_replaces[keyval[0]] = keyval[1].replace(r"\n", "\n")
        elif len(keyval) == 1 and keyval[0] != "":
            if keyval[0].startswith(";;"):
                if multiline:
                    print(current_multikey)
                    input_replaces[current_multikey] = current_multival
                multiline = True
                current_multival = ""
                current_multikey = keyval[0].replace(";;", "", 1)
            elif multiline:
                current_multival += keyval[0] + "\n"
            else:
                raise Exception("what")
                
                    
                    
                    
                


def parse_content(content, ext):
    if ext == ".textile":
        return textile.textile(content)
    elif ext == ".md":
        return pypandoc.convert_text(content, "html5", format="md")
    else:
        raise Exception("Can't recognize the extension in " + os.join(subdir, file))
        return ""