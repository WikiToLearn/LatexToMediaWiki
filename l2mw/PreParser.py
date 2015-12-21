import re
from utility import *

def preparse_tex(tex,print_path):
	#preparse theorem
	th_dict = {}
	tex,th_dict = preparseTheorems(tex)
	#add paragraph after envirmoments
	tex = add_par_after_env(tex,'theorem')
	tex = add_par_after_env(tex,'proof')
	#preparsing labels and refs
	tex = preparserLabels(tex)

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
			continue
		tex = tex.replace(r_match.group(0),u'\\ref{'+label_dict[r_label]+'}')
		#searching all refs
	er = re.compile(ur'\\eqref\s*\{\s*(.*?)\s*\}')
	for er_match in re.finditer(er,tex):
		er_label = er_match.group(1)
		#replacing with new label
		if er_label not in label_dict:
			print("ERROR: label not found: "+ er_label)
			continue
		tex = tex.replace(er_match.group(0),u'\\ref{'+label_dict[er_label]+'}')
	#searching for vref
	vr = re.compile(ur'\\vref\s*\{\s*(.*?)\s*\}')
	for vr_match in re.finditer(vr,tex):
		vr_label = vr_match.group(1)
		#replacing with new label
		if vr_label not in label_dict:
			print("ERROR: label not found: "+ vr_label)
			continue
		tex = tex.replace(vr_match.group(0),u'\\ref{'+label_dict[vr_label]+'}')
	#searching all pageref
	pr = re.compile(ur'\\pageref\s*\{\s*(.*?)\s*\}')
	for pr_match in re.finditer(pr,tex):
		pr_label = pr_match.group(1)
		#replacing with new label
		if pr_label not in label_dict:
			print("ERROR: label not found: "+ pr_label)
			continue
		tex = tex.replace(pr_match.group(0),u'\\ref{'+label_dict[pr_label]+'}')
	return tex