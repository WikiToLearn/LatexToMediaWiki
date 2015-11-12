import re

'''Function that searches \newtheorem command in tex source to find
the theorems environments used. It memorizes them and it normalize them with 
our theorem env'''
def preparseTheorems(tex,print_path):
	th_dict = {}
	p = re.compile(ur'\\newtheorem\*?\{(.*?)\}(\[.*?\])?\{(.*?)\}')
	for match in re.finditer(p,tex):
		print('MATCHED_THM:', match.group(1),match.group(3))
		th_dict[match.group(1)]= match.group(3)
	
	#now we search for every theorem \beging{th_id} and \end{th_id}
	#and we substitue them with \begin{theorem}{th_id} and \begin{theorem}
	#to use out theorem environment
	for key in th_dict:
		tag_open = u'\\begin{'+key+'}'
		new_tag_open = u'\\begin{theorem}{'+key+'}'
		tex = tex.replace(tag_open, new_tag_open)
		tag_close = u'\\end{'+key+'}'
		#the final \n is usefull to create a new par node 
		#for text after theorem
		new_tag_close = u'\\end{theorem}\n'
		tex = tex.replace(tag_close, new_tag_close)

	if(print_path != ""):
		o = open(print_path,"w")
		o.write(tex)
		o.close()
	return (tex, th_dict)


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

