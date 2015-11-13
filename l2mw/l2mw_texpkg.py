from plasTeX import Command,Environment, Macro

class theorem(Environment):
    args = 'th_id:str [th_name:str]' 

class proof(Environment):
	args = '[proof_name:str]'

class vref(Command):
    args='label'

class eqref(Command):
	args = 'label'