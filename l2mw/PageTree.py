# -*- coding: utf-8 -*-
from Page import Page
import datetime,time,re,os
from xml.sax.saxutils import escape
from utility import *


''' Class that memorize the pages' structure and content during parsing '''
class PageTree (object):

	''' The constructor requires the document name.
		-self.keywords is a dictionary with localized keywords for output
		-self.current handles the working section during parsing.
		-self.current_url handles the current url
		-self.pages is a dictionary of pages. The keys are internal url of pages.
		-self.media_urls is a dictionary internal_url = media_url
		-self.labels is a dictionary for label: label=media_url 
		-self.figures contains the list of figure objects
		-self.tables contains the list of table objects
		-self.page_stack contains the history of enviroment until the one before the current'''
	def __init__(self, doc_title, keywords):
		self.doc_title= doc_title
		self.keywords = keywords
		self.pages = {}
		self.media_urls = {}
		self.labels = {}
		#lists of figures and tables
		self.figures = []
		self.tables = []
		self.theorems =[]
		#ROOT PAGE
		r = Page(doc_title,doc_title,doc_title,'root',-1,self.keywords)
		self.pages[doc_title]= r
		#indexes
		self.page_stack = []
		self.pageurl_stack = []
		self.current = doc_title
		self.current_url = doc_title
		#collapse level
		self.collapse_level = 0


	''' This method creates a new page and enters 
	in his enviroment setting current variables'''
	def createPage(self, title,page_type):
		#starting elaboration
		title_name = title[:]
		#remove math tag
		title = self.getNormalizedUrl(title)
		#new url
		newurl = self.current_url+"/"+title
		#finding level
		level = len(self.page_stack)
		#create new page	
		p = Page(title,title_name,newurl,page_type,level,self.keywords)
		#add page to pages index
		self.pages[newurl] = p
		#updates current
		self.page_stack.append(self.current)
		self.pageurl_stack.append(self.current_url)
		self.current= title
		self.current_url= newurl

	'''Function that removes math from title'''
	def getNormalizedUrl(self,title):
		mre = re.search('<\s*math\s*>(.*?)<\s*\/\s*math\s*>',title,re.DOTALL)
		if mre:
			return title.replace(mre.group(0),mre.group(1))
		else:
			return title

	'''This method insert text in the current page   '''
	def addText(self,text):
		self.pages[self.current_url].addText(text)

	'''This method insert a page in the current page's index. It's used when 
 	subsection is encountered'''
	def addToSubpageIndex(self,title):
		self.pages[self.current_url].addSubpage(self.current_url+'/'+\
			self.getNormalizedUrl(title))

	'''Return to the parent page enviroment'''
	def exitPage(self):
		self.current = self.page_stack.pop()
		self.current_url= self.pageurl_stack.pop()

	'''Add label to the current page enviroment'''
	def addLabel(self,label):
		#convert label to int
		label = int(label)
		self.labels[label]= self.current_url

	'''This method return the media_url of the section closer to the label''' 
	def getRef(self,label):
		return self.media_urls[self.labels[label]]

	'''This method add the figure to the figures list. (DO NOT handle the label) '''
	def addFigure(self,figure):
		self.figures.append(figure)
		figure.addPageUrl(self.current_url)

	'''This method add the table_name to the tables dictionary. 
	It's related values is it's page url'''
	def addTable(self,table):
		self.tables.append(table)
		table.addPageUrl(self.current_url)

	current_theorem = None
	'''Method that insert a theorem in the page'''	
	def addTheorem(self, title):
		t = Theorem(title, self.current_url)
		self.current_theorem= t
		self.theorems.append(t)

	def addLabel_insideTheorem(self,label):
		label = int(label)
		self.current_theorem.labels.append(label)

	''' This method collapse the text contained in subpages 
	in the pages with level > level_min.
	The pages with level<level_min is inserted an index of subpages. 
	After text collapsing the mediawiki url for each page is
	computed as needed. Label references are updated'''
	def collapseText(self,level_max):
		self.collapse_level = level_max
		#collapsing text
		self.pages[self.doc_title].collapseText(level_max,self.pages)
		#collapsing mediawiki url
		self.pages[self.doc_title].collapseMediaURL(level_max,self.pages,self.media_urls,'',{})

		#FIXING URLS FROM INTERNAL TO MEDIAWIKIURL
		#fixing labels with mediawikiurls
		for l in self.labels:
			self.labels[l] = self.media_urls[self.labels[l]]
		#fixing figures mediaurls
		for f in self.figures:
			f.page_url = self.media_urls[f.page_url]
		#fixing tables mediaurls
		for t in self.tables:
			t.page_url = self.media_urls[t.page_url]
		#fixing theorems media_url
		for thm in self.theorems:
			murl = self.media_urls[thm.internal_url]
			murl +=  "#"+thm.title
			thm.media_url= murl
			#adding labels inside theorem to labels dict
			for lt in thm.labels:
				self.labels[lt]= murl

	'''Method that starts the rendering of refs'''
	def fixReferences(self):
		self.pages[self.doc_title].fixReferences(self.labels,self.pages)

	'''index for book export page'''
	book_export_index = ['{{libro_salvato | setting-papersize = a4\
 				| setting-toc = auto | setting-columns = 1}}']

	'''Method that creates the index in the root page and the 
	index for book export page'''
	def createIndex(self,max_level):
		ind = ''
		base_page = self.pages[self.doc_title]
		base_page.text += '{{RiferimentiEsterni \
		|esercizi= \n|dispense=\n|testi=}}\n'
		#book export: link
		base_page.text+= '{{libro|Project:Libri/'+self.doc_title+\
				'|'+ self.doc_title + '}}\n'
		#book export: setting title
		self.book_export_index.append('=='+ self.doc_title+'==')
		#creating root index
		base_page.text+= '\n\n==' +self.keywords['chapters']+'==\n'
		base_page.text+= self._createIndex(self.doc_title,'',max_level) 
		#creating book export page
		book_title = 'Project:Libri_'+self.doc_title
		book_export_page= Page(book_title,book_title,
			'Project:Libri/'+self.doc_title,'root',-1,None)
		#inserting index text
		book_export_page.addText(u'\n'.join(self.book_export_index))
		#the export book page is inserted in the pages dict and index
		self.pages['Project:Libri/'+self.doc_title] = book_export_page

	def _createIndex(self,page,ind,max_level):
		index = []
		for sub in self.pages[page].subpages:
			p = self.pages[sub]
			#managing chapters
			if p.level ==0:
				index.append('{{Section\n|sectionTitle=')
				index.append(p.title_name+'\n')
				index.append('|sectionText=\n')
				#book export index for chapters
				self.book_export_index.append(';'+ p.title_name)
				if p.text != '':
					index.append('*[['+ sub+'|Introduzione]]\n')
					self.book_export_index.append(':[['+ sub+']]')

			elif p.text !='':
				index.append(ind+'[['+ sub+'|'+ p.title_name+']]\n')
				self.book_export_index.append(':[['+ sub+']]')
			else:
				index.append(ind + p.title_name + '\n')
			#next level
			if(self.pages[page].level<max_level-1):
				index.append(self._createIndex(sub,ind+'*',max_level))
			#closing chapter
			if p.level==0:
				index.append('}}\n{{ForceBreak}}\n')
		return u''.join(index)

	'''Entry point for exporting pages. config is a tuple 
	with (export_format, username, userid)'''
	def exportPages(self, path, config):
		#choosing format
		f = open(path,'w')
		if config[0]=='xml':
			f.write(self.exportXML(config[1],config[2]))
		elif config[0] == 'text':
			f.write(self.exportText())
		f.close()

	'''Entry point to export pages in separated files.'''
	def export_singlePages(self, format,base_path,config=('','')):
		if not os.path.exists(base_path):
			os.makedirs(base_path)
		if format=='xml':
			self.exportXML_single_pages(config[0],config[1],base_path)
		elif format == 'text':
			self.exportText_single_pages(base_path)

	'''Entry point for XML exporting
	-base_path is the base path for all exported pages'''
	def exportXML(self,username,userid):
		self.export_username = username
		self.export_userid = userid
		s = []
		s.append('<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/"\
		 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" \
		 xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.10/\
		  http://www.mediawiki.org/xml/export-0.10.xsd" version="0.10" \
		  xml:lang="it">\
			<siteinfo>\
			<sitename>WikiToLearn - collaborative textbooks</sitename>\
			<dbname>itwikitolearn</dbname>\
			<base>http://it.wikitolearn.org/Pagina_principale</base>\
			<generator>MediaWiki 1.25.2</generator>\
			<case>first-letter</case>\
			<namespaces>\
			<namespace key="-2" case="first-letter">Media</namespace>\
			<namespace key="-1" case="first-letter">Speciale</namespace>\
			<namespace key="0" case="first-letter"/>\
			<namespace key="1" case="first-letter">Discussione</namespace>\
			<namespace key="2" case="first-letter">Utente</namespace>\
			<namespace key="3" case="first-letter">Discussioni utente</namespace>\
			<namespace key="4" case="first-letter">Project</namespace>\
			<namespace key="5" case="first-letter">Discussioni Project</namespace>\
			<namespace key="6" case="first-letter">File</namespace>\
			<namespace key="7" case="first-letter">Discussioni file</namespace>\
			<namespace key="8" case="first-letter">MediaWiki</namespace>\
			<namespace key="9" case="first-letter">Discussioni MediaWiki</namespace>\
			<namespace key="10" case="first-letter">Template</namespace>\
			<namespace key="11" case="first-letter">Discussioni template</namespace>\
			<namespace key="12" case="first-letter">Aiuto</namespace>\
			<namespace key="13" case="first-letter">Discussioni aiuto</namespace>\
			<namespace key="14" case="first-letter">Categoria</namespace>\
			<namespace key="15" case="first-letter">Discussioni categoria</namespace>\
			<namespace key="2600" case="first-letter">Argomento</namespace>\
			</namespaces>\
			</siteinfo>')
		#getting xml for every page
		for page in self.pages.values():
			if page.level <= self.collapse_level:
				s.append(self.getPageXML(page))
		s.append('</mediawiki>')
		return '\n'.join(s)

	'''Return the mediawiki XML of a single page encoded in utf-8'''
	def getPageXML(self,page):
		#check if the page is not void
		if page.text == '':
			return ''
		#escaping xml before export
		text = escape(page.text)
		#construction of page xml
		s =[]
		s.append('<page>\n<title>'+ page.url +'</title>')
		s.append('\n<restrictions></restrictions>')
		s.append('\n<revision>')
		ts = time.time()
		s.append('\n<timestamp>'+ datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
		s.append('</timestamp>')
		s.append('\n<contributor><username>'+self.export_username+'</username>'+
			'<id>'+self.export_userid+'</id></contributor>')
		s.append('\n<model>wikitext</model>')
		s.append('<format>text/x-wiki</format>')
		s.append('\n<text xml:space="preserve">'+ text+'\n</text>')
		s.append('\n</revision>\n</page>')
		result = '\n'.join(s)
		#encoding result
		return result.encode('utf-8')

	'''Function that export the XML dump format of pages in separated fils'''
	def exportXML_single_pages(self,username,userid, base_path=''):
		self.export_username = username
		self.export_userid = userid
		for page in self.pages.values():
			if page.level <= self.collapse_level:
				xml = self.getPageXML(page)
				path = base_path+'/'+page.title+".xml"
				path = path.encode('utf-8')
				f = open(path,'w')
				f.write(xml)
				f.close()

	'''Functions that exports all the pages in our file with
	format usable with pagefromfile.py script'''
	def exportText(self):
		output = []
		for page in self.pages.values():
			if page.level <= self.collapse_level:
				if page.text != "":
					output.append('##########')
					output.append('\'\'\''+ page.url+ '\'\'\'')
					output.append(page.text)
					output.append('@@@@@@@@@@')
		return ('\n'.join(output)).encode('utf-8')
				
	'''Function that exports the text of pages in separated files'''
	def exportText_single_pages(self,base_path=''):
		for page in self.pages.values():
			if page.level <= self.collapse_level:
				text = []
				text.append('##########')
				text.append('\'\'\''+ page.url+ '\'\'\'')
				text.append(page.text)
				text.append('@@@@@@@@@@')
				path = base_path+'/'+page.title+".txt"
				path = path.encode('utf-8')
				f = open(path, 'w')
				f.write(('\n'.join(text)).encode('utf-8'))
				f.close()

class Figure(object):

	def __init__(self,label,caption,filename):
		self.label = label
		self.caption = caption
		self.filename= filename
		self.page_url=''

	def addPageUrl(self,page_url):
		self.page_url = page_url

	def __str__(self):
		s = []
		s.append('Figure|label@'+self.label)
		s.append('|caption@'+ self.caption)
		s.append('|filename@'+self.filename)
		s.append('|pageurl@'+self.page_url)
		return u''.join(s)


class Table(object):

	def __init__(self,label,caption):
		self.label = label
		self.caption = caption
		self.page_url=''
		
	def addPageUrl(self,page_url):
		self.page_url = page_url

	def __str__(self):
		s = []
		s.append('Table|label@'+self.label)
		s.append('|caption@'+ self.caption)
		s.append('|pageurl@'+self.page_url)
		return u''.join(s)

class Theorem(object):

	def __init__(self,title,internal_url):
		self.title = title
		self.labels = []
		self.internal_url = internal_url
		self.media_url = ''