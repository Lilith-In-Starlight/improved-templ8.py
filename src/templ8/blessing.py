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
    
# Misnomer: This is the default blogbase
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


# Checks if a directory exists and make it if not
def makedir(path, warning = ""):
	if not os.path.exists(path):
		if warning != "":
			print("WARNING: " + warning)
		os.mkdir(path)


# Processes the repl8ce of a header
def mod_replaces(input_replaces, header):
	# These variables are used for multiline keys
	current_multikey = "" # The current key being edited
	multiline = False
	
	for i in header.split("\n"):
		# Split it in the single line way
		keyval = i.split("=", 1)
		# If we're not processing multilines, and the current line is single line, set key
		if len(keyval) == 2 and not multiline:
			input_replaces[keyval[0]] = keyval[1].replace(r"\n", "\n")
		# If it's not a valid single line
		elif len(keyval) == 1 and keyval[0] != "":
			# If it's a valid multiline, start a new multiline tag
			if keyval[0].startswith(";;"):
				multiline = True
				current_multikey = keyval[0].replace(";;", "", 1)
				if not current_multikey in input_replaces:
					input_replaces[current_multikey] = ""
			# If it's not, continue the current multiline
			elif multiline:
				input_replaces[current_multikey] += keyval[0] + "\n"
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

	
ifkey_start = "$$IF_"
fkey_end = "$$END$$"


class Token:
	def __init__(self, end, type, text, start):
		self.end = end
		self.type = type
		self.text = text
		self.start = start
	def __repr__(self):
		return f"[ C: {self.start} - {self.end} T: {self.type} Tx: {self.text} ]"
	def __eq__(self, other):
		return (self.end == other.end and self.start == other.start)


def parts(input_base):
	start = 0
	tokens = {}
	while input_base.find(ifkey_start, start) != -1 or input_base.find(fkey_end, start) != -1:
		token_start = 0
		token_end = 0
		token_type = "void"
		if input_base.find(ifkey_start, start) < input_base.find(fkey_end, start) and input_base.find(ifkey_start, start) != -1:
			token_start = input_base.find(ifkey_start, start)
			token_end = input_base.find("$$", token_start + 1) + 2
			token_type = "IF"
		else:
			token_start = input_base.find(fkey_end, start)
			token_end = token_start + len(fkey_end)
			token_type = "END"
			
		
		tokens[token_start] = Token(token_end, token_type, input_base[token_start:token_end], token_start)
		
		start = token_end 
	return tokens


def funkeys(input_base, keys, tokens):
	out = input_base
	tokpos = sorted(tokens.keys())
	index = 0
	for_deletion = []
	while True:
		if index >= len(tokpos):
			break
		ctoken = tokens[tokpos[index]]
		if tokpos[index+1] in tokens:
			ntoken = tokens[tokpos[index+1]]
			if ntoken.type == "END":
				if ctoken.type == "IF":
					if_key = ctoken.text[len(ifkey_start):-2]
					if if_key in keys and keys[if_key] != "":
						for_deletion.append(ctoken)
						for_deletion.append(ntoken)
					else:
						for_deletion.append(Token(ntoken.end, "CONTENT", "aaa", tokpos[index]))
					
					tokpos.pop(index)
					tokpos.pop(index)
					index -= 1
			else:
				index += 1
		if index >= len(tokpos) - 1:
			break
	
	
	if len(for_deletion) > 0:
		delclumps = [for_deletion[0]]
		
		old_delclumps = for_deletion
		while True:
			index = 0
			for tk in old_delclumps:
				ntk_start = tk.start
				ntk_end = tk.end
				if delclumps[index].start >= ntk_start and delclumps[index].end <= ntk_end:
					delclumps[index].start = ntk_start
					delclumps[index].end = ntk_end
				else:
					delclumps.append(Token(ntk_end, "CONTENT", "AAA", ntk_start))
					index += 1
			if old_delclumps == delclumps:
				break
			else:
				old_delclumps = delclumps
				delclumps = [old_delclumps[0]]
				
		delbars = []
		for tk in delclumps:
			start = tk.start
			end = tk.end
			for i in delbars:
				if start > i[0]:
					start -= i[1]
				if end > i[0]:
					end -= i[1]
			out = out[:start] + out[end:]
			delbars.append([start, end - start])
	
	return out
	

def into_html(content, keys, state):
	base = state.basehtml_content
	if "CUSTOMBASE" in keys:
		if os.path.exists(keys["CUSTOMBASE"]):
			base = open(keys["CUSTOMBASE"], "r").read()
		else:
			raise Exception(os.path.join(subdir, file) + " uses a CUSTOMBASE that doesn't exist")
	
	tokens = parts(base)
	if len(tokens) != 0:
		base = funkeys(base, keys, tokens)
	
	
	return base.replace("##CONTENT##", content)