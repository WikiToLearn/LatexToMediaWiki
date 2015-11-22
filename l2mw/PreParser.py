import re
from utility import *

def preparse_tex(tex,print_path):
	#preparse theorem
	th_dict = {}
	tex,th_dict = preparseTheorems(tex)
	#add paragraph after envirmoments
	tex = add_par_after_env(tex,'theorem')
	tex = add_par_after_env(tex,'proof')

	if(print_path != ""):
		o = open(print_path,"w")
		o.write(tex)
		o.close()

	return (tex,th_dict)


'''Function that searches \newtheorem command in tex source to find
the theorems environments used. It memorizes them and it normalize them with 
our theorem env'''
def preparseTheorems(tex):
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
		new_tag_close = u'\\end{theorem}'
		tex = tex.replace(tag_close, new_tag_close)
	return (tex, th_dict)

def add_par_after_env(tex,env):
	return tex.replace('\\end{'+env+'}', '\\end{'+env+'}\n')
