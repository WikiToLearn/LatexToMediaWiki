# -*- coding: utf-8 -*-
import re
from xml.sax.saxutils import escape
from utility import *
import unidecode

''' Class that manages the pages' content '''
class Page(object):

	''' Constructor needs title.
	-self.title is the title normalized for urls
	-self.title_name is the original title (could contains math)
	-self.subpages contains the list of the subpages
	-self.level memorize the level of the page.(root=-1))
	-self.url contains the unique internal url of the page
	-self.type is 'root',part,chapter,section,subsection,subsubection,paragraph.
	-self.keywords is a dictionary with localized keywords for output'''
	def __init__(self,title,title_name,url,page_type,level, keywords ):
		self.title = title
		self.title_name = title_name
		self.url = url
		self.type = page_type
		self.keywords= keywords
		#contains the page text
		self.text = ''
		'''list of subpages urls'''
		self.subpages = []
		self.level = level
		#calculated during collapsing
		self.media_url = ''

	def addText(self,text):
		self.text = text

	def addSubpage(self, ind):
		self.subpages.append(ind)
                    
	''' This method insert the text of subpages in this page if his level is 
	greater than the level parameter.
	It requires the dictionary of pages.'''
	def collapseText(self,max_level,pages_dict):
		#first of all the text is fixed
		self.fix_text_characters()
		#start collapsing
		if(self.level<max_level):
			for subpage in self.subpages:
				pages_dict[subpage].collapseText(max_level,pages_dict)
			#the subpages'index is created if not level =-1 and if the
			#page has text 
			if self.text != '':
				#added refs tags to show footnotes
				self.text+='\n<references/>'
				if self.subpages and self.level !=-1:
					self.text +='\n<noinclude>\n=='+self.keywords['subpages']+'=='
					for p in self.subpages:
						if pages_dict[p].text != '':
							self.text += '\n*[['+p+'|'+pages_dict[p].title_name+']]'
					self.text+= '\n</noinclude>'	
		else:
			#we have to managed the text
			for subpage in self.subpages:
				t = pages_dict[subpage].collapseText(max_level,pages_dict)
				#add text
				self.text+= '\n'+t
			if self.level ==max_level:
				#added refs tags to show footnotes
				self.text+='\n<references/>'
			elif self.level>max_level:
				#Creation of current page'title
				tit = '\n'+'='*(self.level-max_level+1)+self.title_name+'='*(self.level-max_level+1)
				self.text = tit+ "\n"+ self.text
				#return the text
				return self.text

	''' This method collapse internal url of pages in mediawiki_url'''
	def collapseMediaURL(self,max_level,pages_dict,mediaurl_dic,last_url,url_dic):
		if(self.level<max_level):
			last_url = self.url
			#saving mediaurl
			mediaurl_dic[self.url] = self.media_url = self.url
			#managing subspace
			for subpage in self.subpages:
				pages_dict[subpage].collapseMediaURL(max_level,pages_dict,\
					mediaurl_dic,last_url,url_dic)
		else:
			if self.level==max_level: 
				last_url = self.url
				#saving mediawikiurl
				self.media_url= self.url
				mediaurl_dic[self.url] = self.media_url
			else:
				#creation of media-wiki url
				murl = last_url+'#'+self.title
				if murl in url_dic:
					nused = url_dic[murl]
					murl+= '_'+str(nused+1)
					url_dic[murl]+=1
				#saving mediawiki url
				self.media_url= murl
				mediaurl_dic[self.url]=murl
			#managing subpages
			for subpage in self.subpages:
				pages_dict[subpage].collapseMediaURL(max_level,pages_dict,\
					mediaurl_dic,last_url,url_dic)


	'''This method insert the right mediawikiurl in 
	the \ref tags after the collapsing'''
	def fixReferences(self, labels, pages):
		for label in re.findall(ur'\\ref{(.*?)}', self.text):
			#convert label to int
			label_n = int(label)
			self.text = self.text.replace('\\ref{'+label+'}',\
				' ([[' + labels[label_n] + ']]) ')
		for sub in self.subpages:
			pages[sub].fixReferences(labels,pages)
			
	'''Utility function to fix apostrophes and other characters 
	inside the text of the page'''
	def fix_text_characters(self):
		#fix for double apostrophes quotes
		s = re.findall(u'(\`\`)\s?(.*?)\s?(\'\')', self.text, re.DOTALL)
		for item in s:
			self.text = self.text.replace(unicode(item[0]),'"')
		 	self.text = self.text.replace(unicode(item[2]),'"')
		s2 = re.findall(u'(\‘\‘)\s?(.*?)\s?(\’\’)', self.text, re.DOTALL)
		for item2 in s2:
			self.text = self.text.replace(unicode(item2[0]),'"')
		 	self.text = self.text.replace(unicode(item2[2]),'"')
		#apostrophe fixed
		self.text = self.text.replace(u'’',u"'")
		self.text = self.text.replace(u'`',u"'")

	def __str__(self):
		s =[]
		s.append('title='+self.title)
		s.append('title_name='+self.title_name)
		s.append('url='+self.url)
		s.append('media_url='+ self.media_url)
		s.append('subpages='+str(self.subpages))
		s.append('level='+str(self.level))
		return '  '.join(s)