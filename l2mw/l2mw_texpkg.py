from plasTeX import Command,Environment, Macro

class theorem(Environment):
    args = 'th_id:str [th_title:str]' 

class proof(Environment):
	args = '[proof_name:str]'

class vref(Command):
    args='label'

class eqref(Command):
	args = 'label'

class empheq(Environment):
	pass

class cases(Environment):
	pass

class tikzpicture(Environment):
	args = '[options]'

class tikz(Command):
	args = '[options]'
