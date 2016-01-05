from plasTeX import Command,Environment, Macro

class theorem(Environment):
    args = 'th_id:str [th_title:str]' 

class proof(Environment):
	args = '[proof_name:str]'

class vref(Command):
    args='label'

class eqref(Command):
	args = 'label'

class tikzpicture(Environment):
	args = '[options] code'

class tikz(Command):
	args = '[options]'

class lstlisting(Environment):
	args = '[options]'

class lstset(Command):
	args = 'args'

class minted(Environment):
	args = '[options]'

class lstdefinestyle(Command):
        args = 'name args'