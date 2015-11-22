### UTILITY FUNCTIONS ###
from string import *
import json

'''This function remove a command live \command{content}, leaving 
the command untouched, even if it contains nested brakets'''
def remove_command_greedy(tex,command,repl=''):
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
				#we can get che content of outer {}
				result+=repl+ tok[1:pos] + ' '+ tok[pos+1:]+repl
				break;
	return result;

'''This function get the content of the first occurence of the command
\command{content}'''
def get_content_greedy(tex,command):
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