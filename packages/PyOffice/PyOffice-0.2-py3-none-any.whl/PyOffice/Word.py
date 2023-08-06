from .Suite import Suite

class WordProcessor(Suite):

	def __init__(self, process_id):
		self.process_id = process_id
        
	def check_length(self, x):
		return len(x)
