import re
from utility import *

def preparse_tex(tex,print_path):
	#remove commands
	tex = remove_commands(tex,['\\index'])
	#remove centering inside table
	tex = remove_center_inside_table(tex)
	#preparse theorem
	th_dict = {}
	tex,th_dict = preparseTheorems(tex)
	#add paragraph after envirmoments
	tex = add_par_after_env(tex,'theorem')
	tex = add_par_after_env(tex,'proof')
	#preparsing labels and refs
	tex = preparserLabels(tex)
	#removing pspicture
	tex = remove_environment_greedy(tex,'\\pspicture',True)
	#replacing empheq with normal environments
	tex = replace_empheq(tex)
	#printing preparser tex
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

'''Function that replace labels and references with int. This make more simple
the identification of label in the rendere'''
def preparserLabels(tex):
	label_dict = {}
	i = 0
	#searching all labels
	l = re.compile(ur'\\label\s*\{\s*(.*?)\s*\}')
	for match in re.finditer(l,tex):
		label= match.group(1)
		if label not in label_dict:
			label_dict[label]= unicode(i)
			i+=1
		#replacing new label
		tex = tex.replace(match.group(0), u'\\label{'+label_dict[label]+ '}')
		print("LABEL: "+ label + "@"+ label_dict [label])
	#searching all refs
	r = re.compile(ur'\\ref\s*\{\s*(.*?)\s*\}')
	for r_match in re.finditer(r,tex):
		r_label = r_match.group(1)
		#replacing with new label
		if r_label not in label_dict:
			print("ERROR: label not found: "+ r_label)
			tex = tex.replace(r_match.group(0),u'\\ref{-1}')
			continue
		tex = tex.replace(r_match.group(0),u'\\ref{'+label_dict[r_label]+'}')
		#searching all refs
	er = re.compile(ur'\\eqref\s*\{\s*(.*?)\s*\}')
	for er_match in re.finditer(er,tex):
		er_label = er_match.group(1)
		#replacing with new label
		if er_label not in label_dict:
			print("ERROR: label not found: "+ er_label)
			tex = tex.replace(er_match.group(0),u'\\ref{-1}')
			continue
		tex = tex.replace(er_match.group(0),u'\\ref{'+label_dict[er_label]+'}')
	#searching for vref
	vr = re.compile(ur'\\vref\s*\{\s*(.*?)\s*\}')
	for vr_match in re.finditer(vr,tex):
		vr_label = vr_match.group(1)
		#replacing with new label
		if vr_label not in label_dict:
			print("ERROR: label not found: "+ vr_label)
			tex = tex.replace(vr_match.group(0),u'\\ref{-1}')
			continue
		tex = tex.replace(vr_match.group(0),u'\\ref{'+label_dict[vr_label]+'}')
	#searching all pageref
	pr = re.compile(ur'\\pageref\s*\{\s*(.*?)\s*\}')
	for pr_match in re.finditer(pr,tex):
		pr_label = pr_match.group(1)
		#replacing with new label
		if pr_label not in label_dict:
			print("ERROR: label not found: "+ pr_label)
			tex = tex.replace(pr_match.group(0),u'\\ref{-1}')
			continue
		tex = tex.replace(pr_match.group(0),u'\\ref{'+label_dict[pr_label]+'}')
	return tex

'''Function that remove the list of command cmds from tex'''
def remove_commands(tex,cmds):
	for cmd in cmds:
		tex = remove_command_greedy(tex,cmd,True)
	return tex

'''Function that removes centering command inside table environment'''
def remove_center_inside_table(tex):
	pattern = re.compile(ur'\\begin\s*\{\s*table\s*\}(.*?)\\end\s*\{\s*table\s*\}',re.DOTALL)
	for match in re.finditer(pattern,tex):
		#get content of center command
		content = match.group(1)
		content = remove_environment_greedy(content, '\\center')
		content = content.replace('\\centering','')
		#replacing conent without center
		content = '\\begin{table}'+content+'\\end{table}'
		tex = tex.replace(match.group(0), content)
	return tex

'''Function that removes empheq env replacing it with 
the right \begin{env}\end{env}'''
def replace_empheq(tex):
	#searching for all empheq
	while True:
		env = get_environment_content(tex,'empheq')
		print(env)
		if env[0] == '':
			break
		content = env[0]
		match = re.search(ur'\[box=(.*?)]\s*\{(.*?)\}',content,re.DOTALL)
		if match:
			content = content.replace(match.group(0),u'')
			content = '\\begin{'+match.group(2)+'}'+content+'\\end{'+match.group(2)+'}'
			tex = tex.replace(env[1], content)
		pass
	return tex
