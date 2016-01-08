### UTILITY FUNCTIONS ###
from string import *
import re, string,json

'''This function remove a command like \command{content}
 even if it contains nested brakets. If delete_content=False it leaves
 the content of the command without the command, otherwise it deletes all'''
def remove_command_greedy(tex,command,delete_content=False):
	result=''
	tokens = tex.split(command)
	#Remove the fist token that doesn't contain data and save it
	result+= tokens[0]
	#removing spaces at the begin of tokens
	tokens = map(lstrip,tokens[1:])
	#analyzing each token
	for tok in tokens:
		level = 0
		pos = -1
		for ch in tok:
			pos+=1
			if ch=='{':
				level+=1
			elif ch=='}':
				level-=1
			#now check if we are returned to 0 level
			if level ==0:
				if not delete_content:
					#we can get the content of outer {}
					result+= tok[1:pos] + ' '+ tok[pos+1:]
				else:
					result+= ' '+ tok[pos+1:]
				break;
	return result;

''' This function replace a command with the repl par. It must be used 
with command with {}, not with declaration. It understands nested brakets.
If rm_content is true che content of the command and {} are removed'''
def replace_command_greedy(tex,command, repl, rm_content=False,
							  left_delim='{',right_delim='}'):
	result=''
	tokens = tex.split(command)
	#Remove the fist token that doesn't contain data and save it
	result+= tokens[0]
	#removing spaces at the begin of tokens
	tokens = map(lstrip,tokens[1:])
	#analyzing each token
	for tok in tokens:
		level = 0
		pos = -1
		for ch in tok:
			pos+=1
			if ch=='{':
				level+=1
			elif ch=='}':
				level-=1
			#now check if we are returned to 0 level
			if level ==0:
				if rm_content:
					result+=repl+' '+ tok[pos+1:]
				else:
					result+= repl + left_delim+ tok[1:pos]+ \
							right_delim+' '+ tok[pos+1:]
				break;
	return result;

'''This function get the content of the first occurence of the command
\command{content}'''
def get_content_greedy(tex,command):
	if tex.find(command)==-1: 
		return ''
	tok = tex.split(command)[1].lstrip()
	level = 0
	pos = -1
	for ch in tok:
		pos+=1
		if ch=='{':
			level+=1
		elif ch=='}':
			level-=1
		#now check if we are returned to 0 level
		if level ==0:
			#we can get che content of outer {}
			return tok[1:pos]

'''This funcion get a list of content of all \command{content}'''
def get_content_list_greedy(tex,command):
	tokens = tex.split(command)
	#Remove the fist token that doesn't contain data and save it
	result=[]
	tokens = map(lstrip,tokens[1:])
	for tok in tokens:
		level = 0
		pos = -1
		for ch in tok:
			pos+=1
			if ch=='{':
				level+=1
			elif ch=='}':
				level-=1
			#now check if we are returned to 0 level
			if level ==0:
				#we can get che content of outer {}
				result.append(tok[1:pos])
	return result

'''Function that returns the content of the first occurence
of the environment env and all the matched environment in a tuple.
If the env is not found it return ('')'''
def get_environment_content(tex,env, remove_options=False):
	#search \begin and end \tag
	if remove_options:
		pattern = ur'\\begin\s*\{\s*'+env+ \
			ur'\s*\}\s*\[.*?\](.*?)\\end\s*\{\s*'+env+ur'\s*\}'
	else:
		pattern = ur'\\begin\s*\{\s*'+env+ \
				ur'\s*\}(.*?)\\end\s*\{\s*'+env+ur'\s*\}'
	env_result = re.search(pattern,tex,re.DOTALL)
	if env_result:
		return (env_result.group(1), env_result.group(0))
	else:
		return ('','')

'''Function that returns a tuple. Each second member is the content 
of the specified environment'''
def environment_split(tex,env, remove_options=False):
	#search \begin and end \tag
	pattern = ur'\\begin\s*\{\s*'+env+ \
			ur'\s*\}(.*?)\\end\s*\{\s*'+env+ur'\s*\}'
	content = re.split(pattern, tex, flags=re.DOTALL)
	return content

'''Function that removes all the occurences of an environment 
from tex, leaving or not the content.'''
def remove_environment_greedy(tex,env,delete_content=False):
	#search \begin and end \tag
	pattern = ur'\\begin\s*\{\s*'+env+ \
			ur'\s*\}(.*?)\\end\s*\{\s*'+env+ur'\s*\}'
	for env_result in re.finditer(pattern,tex):
		if env_result:
			if delete_content:
				tex =  tex.replace(env_result.group(0),'')
			else:
				tex =  tex.replace(env_result.group(0),env_result.group(1))
	return tex
