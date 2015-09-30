import re

''' Class that manages the pages' content '''
class Page(object):

	''' Constructor needs title.
	-self.subpages contains the list of the subpages
	-self.level memorize the level of the page.(root=-1))
	-self.url contains the unique internal url of the page
	-self.type is 'root',part,chapter,section,subsection,subsubection,paragraph.'''
	def __init__(self,title,url,page_type,level):
		self.title = title
		self.url = url
		self.type = page_type
		#contains the page text
		self.text = ''
		'''list of subpages urls'''
		self.subpages = []
		self.level = level
		#calculated during collapsing
		self.media_url = ''

	def addText(self,text):
		self.text = text

	def addIndex(self, ind):
		self.subpages.append(ind)

	''' This method insert the text of subpages in this page if his level is 
	greater than the level parameter.
	It requires the dictionary of pages.'''
	def collapseText(self,max_level,pages_dict):
		if(self.level<max_level):
			for subpage in self.subpages:
				pages_dict[subpage].collapseText(max_level,pages_dict)
			#the subpages'index is created
			if self.subpages:
				self.text+='\n\n==Sottopagine=='
				for p in self.subpages:
					self.text += '\n*[['+p+']]'
			#added refs tags to show footnotes
			self.text+='\n<references/>'
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
				tit = '\n'+'='*(self.level-max_level+1)+self.title+'='*(self.level-max_level+1)
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
		for label in re.findall(r'\\ref{(.*?)}', self.text): 
			self.text = self.text.replace(unicode('\\ref{'+label+'}'),' ([[' + labels[label] + ']]) ')
		for sub in self.subpages:
			pages[sub].fixReferences(labels,pages)
			

	def __str__(self):
		s =[]
		s.append('title='+self.title)
		s.append('url='+self.url)
		s.append('media_url='+ self.media_url)
		s.append('subpages='+str(self.subpages))
		s.append('level='+str(self.level))
		return '  '.join(s)