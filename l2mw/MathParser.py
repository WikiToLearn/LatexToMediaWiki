# -*- coding: utf-8 -*-
import string,re
from PageTree import *
from utility import *

'''Function that removes $$..$$ and \[...\]'''
def get_content_display_math(tex):
	content = ''
	tag_search = re.search(ur'\$\$(.*?)\$\$|\\\[(.*?)\\\]', tex,re.DOTALL)
	if tag_search:
		if tag_search.group(1):
			content = tag_search.group(1)
		elif tag_search.group(2):
			content = tag_search.group(2)
	return content

'''Functions that removes $...$ and \(...\)'''
def get_content_inline_math(tex):
	content = ''
	tag_search = re.search(ur'\$(.*?)\$|\\\((.*?)\\\)', tex,re.DOTALL)
	if tag_search:
		if tag_search.group(1):
			content = tag_search.group(1)
		elif tag_search.group(2):
			content = tag_search.group(2)
	return content

'''Function that extracts and removes the label from the tex.
it returns a tuple (label, tex)'''
def get_label(tex):
    label_re = re.search(ur'\\\blabel\b\{(.*?)\}', tex)
    label = ''
    if label_re:
        label = label_re.group(1)
        tex = tex.replace(label_re.group(0),"")
    return (label,tex)

'''Function that remove and replace some commands from math'''
def math_check(mtxt):
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
        #replace intertext with mbox
        mtxt = replace_command_greedy(mtxt, '\\intertext', '\\mbox', False)
        #symbols
        mtxt = mtxt.replace('\\abs','|')
        mtxt = mtxt.replace('\\lvert','|')
        mtxt = mtxt.replace('\\rvert','|')
        mtxt = replace_command_greedy(mtxt,'\\modul','|',False,'|','|')
        #removing \nonumber command
        mtxt = mtxt.replace('\\nonumber','')
        mtxt = mtxt.replace('\\notag','')
        #replacing spacing commands
        mtxt = mtxt.replace('\\:','\\,')
        #removing rule command
        rule_match = re.search(ur'\\rule\s*(\[(.*?)\])?(\s*(\{(.*?)\}))*',mtxt)
        if rule_match:
            mtxt = mtxt.replace(rule_match.group(0),'')
        #removing makebox[]{} command
        mtxt = re.sub(ur'\\makebox\s*(\[(.*?)\])*\s?\{(.*?)\}','',mtxt)

        return mtxt