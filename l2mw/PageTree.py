from Page import Page
import datetime
import time
import re
from xml.sax.saxutils import escape


''' Class that memorize the pages' structure and content during parsing '''
class PageTree (object):

	''' The constructor requires the document name.
		-self.current handles the working section during parsing.
		-self.current_url handles the current url
		-self.pages is a dictionary of pages. The keys are internal url of pages.
		-self.media_urls is a dictionary internal_url = media_url
		-self.labels is a dictionary for label: label=media_url 
		-self.figures contains the list of figure objects
		-self.tables contains the list of table objects
		-self.page_stack contains the history of enviroment until the one before the current'''
	def __init__(self, doc_title):
		self.doc_title= doc_title
		self.index = {}
		self.pages = {}
		self.media_urls = {}
		self.labels = {}
		#lists of figures and tables
		self.figures = []
		self.tables = []
		#ROOT PAGE
		self.index[doc_title]={}
		r = Page(doc_title,doc_title,doc_title,'root',-1)
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
		title_name = title[:]
		#remove math tag
		title = self.getNormalizedUrl(title)
		#new url
		newurl = self.current_url+"/"+title
		#finding level
		level = len(self.page_stack)
		#create new page	
		p = Page(title,title_name,newurl,page_type,level)
		#update index
		cindex = self.index
		for i in range(0,len(self.page_stack)):
			cindex = cindex[self.page_stack[i]]
		cindex = cindex[self.current]
		#now cindex has the current dict
		#and new key is inserted
		cindex[title]={}
		#add pages to pages index
		self.pages[newurl] = p
		#updates current
		self.page_stack.append(self.current)
		self.pageurl_stack.append(self.current_url)
		self.current= title
		self.current_url= newurl

	def getNormalizedUrl(self,title):
		mre = re.search('<\s*math\s*>(.*?)<\s*\/\s*math\s*>',title,re.DOTALL)
		if mre:
			return title.replace(mre.group(0),mre.group(1))
		else:
			return title

	'''This method insert text in the current page   '''
	def addText(self,text):
		#print('ADDING TEXT TO URL='+unicode(self.current_url)+' | ADDING TEXT='+unicode(text) +\
			#' |current url='+unicode(self.current_url)+ '|current='+unicode(self.current) )
		self.pages[self.current_url].addText(text)

	'''This method insert a page in the current page's index. It's used when 
 	subsection is encountered'''
	def addToSubpageIndex(self,title):
		self.pages[self.current_url].addIndex(self.current_url+'/'+\
			self.getNormalizedUrl(title))

	'''Return to the parent page enviroment'''
	def exitPage(self):
		self.current = self.page_stack.pop()
		self.current_url= self.pageurl_stack.pop()

	'''Add label to the current page enviroment'''
	def addLabel(self,label):
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

	''' This method collapse the text contained in subpages 
	in the pages with level > level_min.
	The pages with level<level_min is inserted an index of subpages. '''
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
		#fixing figures urls
		for f in self.figures:
			f.page_url = self.media_urls[f.page_url]
		#fixing tables urls
		for t in self.tables:
			t.page_url = self.media_urls[t.page_url]

	'''Method that starts the rendering of refs'''
	def fixReferences(self):
		self.pages[self.doc_title].fixReferences(self.labels,self.pages)

	'''Entry point for XML exporting
	-base_path is the base path for all exported pages'''
	def exportXML(self,base_path=''):
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
		#starting iteration
		if base_path!='':
			self.base_path = base_path+'/'
		else: self.base_path = ''
		self._exportXML(s,-1,self.index,'')
		s.append('</mediawiki>')
		return '\n'.join(s)

	'''Recursion function to explore the tree during exporting'''
	def _exportXML(self, text, lev,cur_dict, cur_url):
		if lev<= self.collapse_level:
			for key in cur_dict:
				page = None
				if cur_url=='':
					page = self.pages[self.doc_title]
				else:
					page = self.pages[cur_url+ '/'+key]

				text.append(self.getPageXML(page))
				if cur_url =='':
					self._exportXML(text,lev+1,cur_dict[key],self.doc_title)
				else:
					self._exportXML(text,lev+1,cur_dict[key],cur_url+"/"+key)

	'''Return the mediawiki XML of a single page'''
	def getPageXML(self,page):
		page.text = escape(page.text)
		page.title= escape(page.title)
		s =[]
		s.append('<page>\n<title>'+escape(self.base_path+page.url)+'</title>')
		s.append('\n<restrictions></restrictions>')
		s.append('\n<revision>')
		ts = time.time()
		s.append('\n<timestamp>'+ datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
		s.append('</timestamp>')
		s.append('\n<contributor><username>Valsdav</username><id>1820</id></contributor>')
		s.append('\n<model>wikitext</model>')
		s.append('<format>text/x-wiki</format>')
		s.append('\n<text xml:space="preserve">'+ page.text+'\n</text>')
		s.append('\n</revision>\n</page>')
		return '\n'.join(s)

	def exportFiguresTables(self,base_path):
		f = open('ft_list',w)
		for fig in self.figures:
			f.write(str(fig))
		for t in self.tables:
			f.write(str(t))
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
