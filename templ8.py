import programstate
import textile
import os
import shutil
import sys
import blessing

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


# Build the blog
def radio():
    state = programstate.ProgramState()
    blog_input = "blog"
    blog_output = os.path.join(state.output_folder, "blog")
    makedir(blog_input)
    makedir(blog_output)
    makedir(os.path.join(blog_output, "posts"))
    article_format_path = "blogbase"
    if not os.path.exists(article_format_path):
        with open(article_format_path, "w") as f:
            f.write(blessing.DEF_BASEHTML_CONTENT)
    
    # The article format is the file that defines how an article will look, both in its own page and in the index
    article_format_page = open(article_format_path, "r").read().split("-BEGININDEX-")[0]
    article_format_index = open(article_format_path, "r").read().split("-BEGININDEX-")[1]
    blog_replacekeys = open(article_format_path, "r").read().split("-BEGININDEX-")[2]
    
    # This is the full index's textile
    blog_index = ""
    
    # Walk through the blog folder
    for subdir, dirs, files in os.walk(blog_input):
        sortedfiles = files
        sortedfiles.sort(reverse = True)
        for file in sortedfiles:
            path = os.path.join(subdir, file)
            file_replace = state.replacements
            # These refer to the individual articles
            file_headers = open(path, "r").read().split("-BEGINFILE-")[0]
            file_content = open(path, "r").read().split("-BEGINFILE-")[1]
            
            # Get the replace keys of the individual article
            for i in file_headers.split("\n"):
                keyval = i.split("=")
                if len(keyval) == 2:
                    file_replace[keyval[0]] = keyval[1]
            
            # This variable refers to the article page with the contents of this individual file
            article_page = article_format_page
            
            # Apply the file's keys to the article page and put in the content
            for key in file_replace:
                article_page = article_page.replace("##"+key+"##", file_replace[key])
            
            article_page = article_page.replace("##CONTENT##", file_content)
            
            # Get the keys and content of this article page
            article_page_headers = article_page.split("-BEGINFILE-")[0]
            article_page_content = article_page.split("-BEGINFILE-")[1]
            
            for i in article_page_headers.split("\n"):
                keyval = i.split("=")
                if len(keyval) == 2:
                    file_replace[keyval[0]] = keyval[1]
            
            # This variable is the final page
            final_page = state.basehtml_content
            
            # Apply the keys of the article page and put in the content
            final_page = final_page.replace("##CONTENT##", textile.textile(article_page_content))
            
            # This one is for the index page, it takes the format and puts the info in
            current_file_index = textile.textile(article_format_index)
            
            current_file_index = current_file_index.replace("##LINK##", 'posts/' + file.replace(".textile", "/index.html"))
            print(current_file_index)
            for key in file_replace:
                final_page = final_page.replace("##"+key+"##", file_replace[key])
                current_file_index = current_file_index.replace("##"+key+"##", file_replace[key])
            blog_index += current_file_index + "\n"
            
            # Save it
            blog_outpath = os.path.join(blog_output, "posts", file.replace(".textile", "/index.html"))
            makedir(os.path.join(blog_output, "posts", file.replace(".textile", "")))
            with open(blog_outpath, "w") as f:
                f.write(final_page)
    
    # Generate the index
    blog_replace = state.replacements.copy()
    for i in blog_replacekeys.split("\n"):
        keyval = i.split("=")
        if len(keyval) == 2:
            blog_replace[keyval[0]] = keyval[1]
    
    index_html = state.basehtml_content
    index_html = index_html.replace("##CONTENT##", blog_index)
    for key in blog_replace:
        index_html = index_html.replace("##"+key+"##", blog_replace[key])
    
    with open(os.path.join(blog_output, "index.html"), "w") as f:
        f.write(index_html)



def help():
    print(blessing.TEMPL8_ASCII + "\n\n")
    print("  help             Display this list.")
    print("  genesis [name]   Create a new templ8 project in a folder named [name].")
    print("  divine           Assemble a templ8 site.")
    print("  radio            Assemble a templ8 blog.")
    print("")

if __name__ == "__main__":    
    if len(sys.argv) <= 1:
        help()
    elif sys.argv[1] == "help":
        help()
    elif sys.argv[1] == "divine":
        divine()
    elif sys.argv[1] == "radio":
        radio()
    elif sys.argv[1] == "genesis":
        if len(sys.argv) >= 3:
            genesis(sys.argv[2])
        else:
            raise Exception("Unexpected number of arguments")
    else:
        raise Exception("Unknown command")
    
