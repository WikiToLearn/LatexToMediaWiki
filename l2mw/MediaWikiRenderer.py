import string,re
from plasTeX.Renderers import Renderer
from PageTree import *

class MediaWikiRenderer (Renderer):

    outputType = unicode
    fileExtension = '.xml'
    lineWidth = 76

    aliases = {
        'superscript': 'active::^',
        'subscript': 'active::_',
        'dollar': '$',
        'percent': '%',
        'opencurly': '{',
        'closecurly': '}',
        'underscore': '_',
        'ampersand': '&',
        'hashmark': '#',
        'space': ' ',
        'tilde': 'active::~',
        'at': '@',
        'backslash': '\\',
        #math starred commmands
        'equation_star':'equation*',
        'eqnarray_star':'eqnarray*',
        'align_star':'align*',
        'alignat_star':'alignat*',
        'multline_star':'multline*',
        'gather_star':'gather*'
    }

    '''List of nodes not to explore'''
    no_enter = ['titlepage','maketitle',
            'numberwithin','geometry']

    def __init__(self, doc_title,*args, **kwargs):
        Renderer.__init__(self, *args, **kwargs)
        #document title
        self.doc_title = doc_title
        # Load dictionary with methods
        for key in dir(self):
            if key.startswith('do__'):
                self[self.aliases[key[4:]]] = getattr(self, key)
            elif key.startswith('do_'):
                self[key[3:]] = getattr(self, key)

        self['default-layout'] = self['document-layout'] = self.default
        self.footnotes = []
        self.blocks = []
        #tree object
        self.tree = PageTree(doc_title)
        #parameter for list formatting
        self.list_level=u'' 

        ####### TAGS ANALYSY
        #set for default tags
        self.def_tags = set()
        #dictionary for tag usage
        self.used_tags = {}

    def default(self, node):
        if node.nodeName in self.no_enter:
            return u''
        s = []
        self.def_tags.add(node.nodeName)
        s.append(unicode(node).lstrip())
        return u''.join(s)


    def do_textDefault(self, node):
        return unicode(node).lstrip()

    ###############################
    #sectioning
    def sectioning(self, node,page_type):
        title = unicode(node.attributes['title'])
        #adding index to parent
        self.tree.addToSubpageIndex(title)
        #creation of the new page
        self.tree.createPage(title,page_type)
        #content processing
        text = unicode(node).lstrip()
        #adding text to current page
        self.tree.addText(text)
        #exiting the section
        self.tree.exitPage()

    def do_part (self,node):
        self.sectioning(node,'part')
        return u''

    def do_chapter (self,node):
        self.sectioning(node,'chapter')
        return u''

    def do_section(self,node):
        self.sectioning(node,'section')
        return u''

    def do_subsection(self,node):
        self.sectioning(node,'subsection')
        return u''

    def do_subsubsection(self,node):
        self.sectioning(node,'subsubsection')
        return u''

    def do_paragraph(self,node):
        self.sectioning(node,'paragraph')
        return u''
    #################################################
    
    #subparagraph are not node of the section tree
    def do_subparagraph(self,node):
        s =[]
        s.append('\n\'\'\'')
        s.append(unicode(node.attributes['title']))
        s.append('\'\'\'\'')
        s.append(unicode(node).lstrip())
        return u''.join(s)
    
    '''Enter point for parsing. Root page is already created'''
    def do_document(self,node):
        content = unicode(node)
        self.tree.addText(content)
        return u'%s' % content


    ###############################################
    #references
    ''' Method that insert label into PageTree'''
    def label(self,lab):
        #the reference to the current page is saved
        self.tree.addLabel(lab)

    ''' Labels are managed bey PageTree'''
    def do_label(self,node):
        #retriving label id
        l = node.attributes['label']
        self.label(l)
        return u''

    '''All ref tag are substituted by normal ref tag.
    It'll be reparsed after text collapsing'''
    def do_ref(self,node):
        r = node.attributes['label']
        return unicode('\\ref{'+r+'} ')

    do_pageref = do_ref
    do_vref = do_ref
    do_eqref = do_ref


    ################################################
    #Formatting
    '''Paragraph'''
    def do_par(self, node):
        s = []
        s.append(u'\n\n')
        s.append(unicode(node).lstrip())
        return u''.join(s)

    '''Breaks line inside a paragraph'''
    def do_newline(self,node):
        return u'<br/>'
    
    do__backslash = do_newline

    def do_textbf(self,node):
        s=[]
        s.append(u"\'\'\'")
        s.append(unicode(node).lstrip())
        s.append(u"\'\'\'")
        return u''.join(s)
        
    def do_textit(self,node):
        s=[]
        s.append(u"\'\'")
        s.append(unicode(node).lstrip())
        s.append(u"\'\'")
        return u''.join(s)    

    do_emph = do_textit
    do_itshape = do_textit
    do_textsl = do_textit
    do_slshape = do_textit
   
    def do_newpage(self,node):
        s = []
        s.append(u'')
        s.append(unicode(node).lstrip())
        return u''.join(s)

    def do_itemize(self,node):
        s = []
        self.list_level+=u'*'
        for item in node.childNodes:
            t=unicode(item).lstrip()
            s.append(self.list_level+t)
        self.list_level = self.list_level[:-1]
        return u'\n'.join(s)

    def do_enumerate(self,node):
        s = []
        self.list_level+=u'#'
        for item in node.childNodes:
            t=unicode(item).lstrip()
            s.append(self.list_level+t)
        self.list_level = self.list_level[:-1]
        return u'\n'.join(s)
    
    def do_description(self,node):
        s = []
        for item in node.childNodes:
            t=unicode(item).lstrip()
            s.append(u';'+ str(item.attributes['term'])+":" +t)
        return u'\n'.join(s)

    def do__tilde(self,node):
        return unicode(node)    

    def do__dollar(self,node):
        return u'$'

    def do__percent(self,node):
        return u'%'

    def do__opencurly(self,node):
        return u'{'

    def do__closecurly(self,node):
        return u'}'
    
    def do__hashmark(self,node):
        return u'#'

    def do__underscore(self,node):
        return u'_'

    def do__ampersand(self,node):
        return u'&'

    def do_quotation(self, node):
        s = []
        s.append(u'<blockquote>')
        s.append(unicode(node)).lstring()
        s.append(u'</blockquote>')
        return u''.join(s)

    do_quote=do_quotation
    do_verse=do_quotation

    def do_centering(self, node):
        s = []
        s.append(u'<div style="text-align:center;">')
        s.append(unicode(node).lstrip())
        s.append(u'</div>')
        return u''.join(s)

    do_center = do_centering

    def do_flushright(self, node):
        s = []
        s.append(u'<div style="text-align:right;">')
        s.append(unicode(node).lstrip())
        s.append(u'</div>')
        return u''.join(s)

    def do_flushleft(self, node):
        return unicode(node).lstrip()

    def do_footnote(self,node):
        s=[]
        s.append(u"<ref>")
        s.append(unicode(node).lstrip())
        s.append(u"</ref>")
        return u''.join(s)

    def do_hrulefill(self,node):
        return u'----'  

    do_rule=do_hrulefill   

    def do_textrm(self, node):
        return unicode(node)

    def do_small(self, node):
        s = []
        s.append(u'<small>')
        s.append(unicode(node).lstrip())
        s.append(u'</small>')
        return u''.join(s)

    do_tiny=do_small
    do_scriptsize=do_small
    
    def do_underline(self, node):
        s = []
        s.append(u'<u>')
        s.append(unicode(node).lstrip())
        s.append(u'</u>')
        return u''.join(s)
    
    do_underbar=do_underline

    def do_texttt(self,node):
        s=[]
        s.append(u"<tt>")
        s.append(unicode(node).lstrip())
        s.append(u"</tt>")
        return u''.join(s)  

    def do_verbatim(self,node):
        s=[]
        s.append(u'<nowiki>')
        s.append(unicode(node.source)).lstrip()
        s.append(u'</nowiki>\n')
        return u''.join(s)
        
    ##########################################
    #figures and tables
    '''The figure environment is handled with regexs. '''
    def do_figure(self,node):
        file_path=''
        caption = ''
        label=''
        #searchin includegraphics
        graphics_search = re.search(ur'\\includegraphics(\[.*\])*{(.*?)}',node.source)
        if graphics_search: 
            file_path= graphics_search.group(2)
        #searching label
        label_search = re.search(ur'\\label{(.*?)}',node.source)
        if label_search:
            label = label_search.group(1)
        #searching caption
        caption_search = re.search(ur'\\caption{(.*?)}',node.source)
        if caption_search:
            caption = caption_search.group(1)
        #creating figure
        f = Figure(label,caption,file_path)
        #adding figure to tree
        self.tree.addFigure(f)
        #adding label
        if label:
            self.label(label)
        #return warning text for figure
        return unicode('[[Figura:'+label+'_'+caption+'_'+file_path+']]')

    '''The Table environment is handled with regex'''
    def do_table(self,node):
        caption = ''
        label = ''
        #searching label
        label_search = re.search(ur'\\label{(.*?)}',node.source)
        if label_search:
            label = label_search.group(1)
        #searching caption
        caption_search = re.search(ur'\\caption{(.*?)}',node.source)
        if caption_search:
            caption = caption_search.group(1)
        #creating table
        t = Table(label,caption)
        #adding table to the tree
        self.tree.addTable(t)
        #adding label
        if label:
            self.label(label)
        #return warning text for table
        return unicode('[[Tabella:'+label+'_'+caption+']]')


    ###################################################
    #Math tags

    '''Handles math insede a displaymath mode:
    -it removes $$ and \[ \].
    -it remove \begin and \end so it has to be used 
    only for \begin{equation} and \begin{displaymath}.
    Other \begin{math_environment} that are not inside a displaymath 
    have to be handled by specific methods'''
    def handleDisplayMath(self, node): 
        begin_tag = ''
        end_Tag = ''     
        split_tag = ''
        label_tag = ''
        structure_label_tag = ''
        s = node.source

        #$$ search
        global_dollars_search = re.search(ur'\$\$(.*?)\$\$', s)
        #search \begin and end \tag
        global_begin_tag = re.search(ur'\\\bbegin\b\{(\bequation\*?)\}|\\\[', s)
        global_end_tag = re.search(ur'\\\bend\b\{(\bequation\*?)\}|\\\]', s)

        #get content between $$ $$
        #get \begin{tag} and \end{tag}
        #and delete the tags
        if global_begin_tag and global_end_tag:
            begin_tag = global_begin_tag.group(0)
            end_tag = global_end_tag.group(0)
            s = s.replace(begin_tag, "")
            s = s.replace(end_tag, "")
        elif global_dollars_search:
            dollars_tag = global_dollars_search.group(1)
            s = s.replace(dollars_tag, "")

        #replace split with align
        s = s.replace("split", u"align")

        #removing inner starred commands
        re_remove_star= re.compile(ur'\\begin{(\w+)\*}(.*?)\\end{(\w+)\*}',re.DOTALL)
        for star_tag in re.finditer(re_remove_star,s):
            s = s.replace(star_tag.group(0),u'\\begin{'+star_tag.group(1)+'}'+\
                star_tag.group(2)+'\end{'+ star_tag.group(3)+'}')
        
        #searching for label
        global_label_tag = re.search(ur'\\\blabel\b\{(.*?)\}', s)
        #getting label and deleting label tag
        if global_label_tag:
            label_tag = global_label_tag.group(1)
            structure_label_tag = global_label_tag.group(0)
        else:
            label_tag = ''
            structure_label_tag = ''
        #deleting label tag
        s = s.replace(structure_label_tag, "")

        s_tag = ''
        if label_tag is not '':
            #adding label to tree
            self.label(label_tag)
            s_tag = '<dmath label="' + label_tag + '">'
        else:
            s_tag = '<dmath>'
        return s_tag + s + '</dmath>'

    do_displaymath = handleDisplayMath
    do_equation = handleDisplayMath
    do__equation_star = handleDisplayMath

    '''Handles inline math ( $..$ \( \) ) '''
    def do_math(self, node):
        content = ''
        s = node.source
        #search content between $ $
        global_tag = re.search(ur'\$(.*?)\$', s)
        #search for \( \)
        regexp_brackets_global_tag = re.compile(ur'\\\((.*?)\\\)', re.DOTALL)
        brackets_global_tag = re.search(regexp_brackets_global_tag,s)

        #get content between $ $ and remove them
        if global_tag:
            content = global_tag.group(1)
        elif brackets_global_tag:
            content = brackets_global_tag.group(1)
        else:
            content = ''

        #removing inner starred commands
        re_remove_star= re.compile(ur'\\begin{(\w+)\*}(.*?)\\end{(\w+)\*}',re.DOTALL)
        for star_tag in re.finditer(re_remove_star,s):
            s = s.replace(star_tag.group(0),u'\\begin{'+star_tag.group(1)+'}'+\
                star_tag.group(2)+'\end{'+ star_tag.group(3)+'}')

        #get content between \begin{split}
        s = s.replace("split", u"align")

        return '<math>'+ content +'</math>'

    do_ensuremath = do_math

    '''Support for align type tags. 
    They are outside math modes an supported directly'''
    def do_align(self, node):
        split_tag = ''
        label_tag = ''
        begin_tag = ''
        end_Tag = ''
        structure_label_tag = ''
        s = node.source
      
        #replace split with align
        s = s.replace("split", u"align")
        #replace eqnarray,multline,alignat with align
        s = s.replace('alignat',u'align')
        s = s.replace('eqnarray',u'align')
        s = s.replace('multline',u'align')
        s = s.replace('gather',u'align')

        #removing inner starred commands
        re_remove_star= re.compile(ur'\\begin{(\w+)\*}(.*?)\\end{(\w+)\*}',re.DOTALL)
        for star_tag in re.finditer(re_remove_star,s):
            s = s.replace(star_tag.group(0),u'\\begin{'+star_tag.group(1)+'}'+\
                star_tag.group(2)+'\end{'+ star_tag.group(3)+'}')
            
        #search equation tag
        global_label_tag = re.search(ur'\\\blabel\b\{(.*?)\}', node.source)
        #getting label and deleting label tag
        if global_label_tag:
            label_tag = global_label_tag.group(1)
            structure_label_tag = global_label_tag.group(0)
        else:
            label_tag = ''
            structure_label_tag = ''
        #deleting label tag
        s = s.replace(structure_label_tag, "")
        
        # check if label tag exist. If it does,
        # insert the tag in output and tree
        s_tag = ''
        if label_tag is not '':
            #adding label to tree
            self.label(label_tag)
            s_tag = '<dmath label="' + label_tag + '">'
        else:
            s_tag = '<dmath>'
        return s_tag + s + '</dmath>'

    do_eqnarray = do_align
    do_multline = do_align
    do_alignat =  do_align
    do_gather = do_align
    #using aliases
    do__align_star = do_align
    do__alignat_star = do_align
    do__eqnarray_star = do_align
    do__multline_star = do_align
    do__gather_star = do_align


    ###############################################
    
    
