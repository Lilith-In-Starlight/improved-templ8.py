import os
import shutil
import textile
import programstate
from blessing import makedir

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
                with open(path, "r") as f:
                    contents = ""
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
                    
                    # Check if the folder is in txignore
                    in_txignore = False
                    for i in state.txignore:
                        if os.path.join(state.input_folder, os.path.normpath(i)) == path or os.path.join(state.input_folder, os.path.normpath(i)) == subdir:
                            in_txignore = True
                            break
                          
                    
                    if not in_txignore:
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
                    else:
                        with open(outpath, "w") as f:
                            f.write(file_content)
                    
                    
                    
            elif not os.path.exists(outpath):
                shutil.copy(path, outpath)
    

    print("Finished assembling")