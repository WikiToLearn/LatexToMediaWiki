from MediaWikiRenderer import MediaWikiRenderer
from XMLRenderer import XMLRenderer
from PreParser import *

### UTILITY FUNCTIONS ###

'''This function remove a command live \command{content}, leaving 
the command untouched, even if it contains nested brakets'''
def greedy_remove_command(tex,command):
	result=''
	tokens = tex.split(command)
	#Remove the fist token that doesn't contain data and save it
	result+= tokens[0]
	tokens = tokens[1:]
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
				result+=tok[1:pos] + ' '+ tok[pos+1:]
				break;
	return result;

	'''This function get the content of the first occurence of the command
	\command{content}'''
	def greedy_get_content(tex,command):
		tok = tex.split(command)[1]
		result=''
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
				result+=tok[1:pos] + ' '+ tok[pos+1:]
		return result

	