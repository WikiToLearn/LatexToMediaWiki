from plasTeX import Command,Environment, Macro

class theorem(Environment):
    args = 'th_id:str [th_name:str]' 

class proof(Environment):
	pass


class vref(Command):
    args='label'

class eqref(Command):
	args = 'label'