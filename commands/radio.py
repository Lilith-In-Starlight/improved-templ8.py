import os
import textile
import programstate
from blessing import makedir

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