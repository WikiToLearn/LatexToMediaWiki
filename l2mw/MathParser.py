# -*- coding: utf-8 -*-
import string,re
from PageTree import *
from utility import *

'''Function that removes $$..$$ and \[...\]'''
def get_content_display_math(tex):
	tag_search = re.search(ur'\$\$(.*?)\$\$|\\\[(.*?)\\\]', tex,re.DOTALL)
	if tag_search:
		return tag_search.group(1)
	else:
		return ''

'''Functions that manipulate inline math.
Return a tuple with (result, label)'''
def inline_math(tex):
	#removing $..$ and \(..\)
	content = ''
	dollar_tag = re.search(ur'\$(.*?)\$', tex)
	open_tag = re.search(ur'\\\((.*?)\\\)', tex)
	if dollar_tag:
		content = dollar_tag.group(1)
	elif:
		content = open_tag.group(1)
	#getting label
	label = get_label(content)
	#checking math
	content = math_check(content)
	return ('<math>'+ content +'</math>',label)

'''Function that extract label from tex'''
def get_label(tex):
	label_re = re.search(ur'\\\blabel\b\{(.*?)\}', tex)
	if(label_re):
		tex = tex.replace(label_re.group(0),"")
		return label_re.group(1)

'''Function that remove and replace some commands from math'''
def math_check(self,mtxt):
         #removing inner starred commands
        re_remove_star= re.compile(ur'\\begin{(\w+)\*}(.*?)\\end{(\w+)\*}',re.DOTALL)
        for star_tag in re.finditer(re_remove_star,mtxt):
            mtxt = mtxt.replace(star_tag.group(0),u'\\begin{'+star_tag.group(1)+'}'+\
                star_tag.group(2)+'\end{'+ star_tag.group(3)+'}')
        #replacing split with align
        mtxt = mtxt.replace(u"split",u"align")
        #removing \boxed command
        mtxt = remove_command_greedy(mtxt,'\\boxed')
        #removing \ensuremath from macros
        mtxt = remove_command_greedy(mtxt,'\\ensuremath')
        #removing tiny command
        mtxt = remove_command_greedy(mtxt,'\\tiny')
        #replace hspace with \quad
        mtxt = replace_command_greedy(mtxt, '\\hspace', '\\quad',True)
        #replacing bb and bbm with boldmath
        mtxt = replace_command_greedy(mtxt, '\\bm','\\mathbf', False)
        mtxt = replace_command_greedy(mtxt, '\\bbm','\\mathbf', False)
        #abs
        mtxt = replace_command_greedy(mtxt, '\\abs','|', False)
        #removing \nonumber command
        mtxt = mtxt.replace('\\nonumber',u'')
        return mtxt