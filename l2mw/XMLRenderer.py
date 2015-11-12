import string,re
from plasTeX.Renderers import Renderer
from PageTree import PageTree

class XMLRenderer(Renderer):


    def __init__(self, *args, **kwargs):
        Renderer.__init__(self, *args, **kwargs)
        # Load dictionary with methods
        for key in dir(self):
            if key.startswith('do_'):
                self[key[3:]] = getattr(self, key)
        self['default-layout'] = self['document-layout'] = self.default
        self.footnotes = []
        self.blocks = []

    def default(nself,node):
        s = []
        s.append('<%s>' % node.nodeName)
        if node.hasAttributes() :
            s.append('<attributes>')
            for key, value in node.attributes.items():
                if key == 'self':
                    continue
                s.append('<%s>%s</%s>\n' % (key,unicode(value),key))
            s.append('</attributes>')

        s.append(unicode(node))
        s.append('</%s>\n' % node.nodeName)
        return u'\n'.join(s)

    def textDefault(self,node):
        return unicode(node).lstrip()

        
   