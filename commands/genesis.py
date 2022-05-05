import os
from blessing import makedir

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