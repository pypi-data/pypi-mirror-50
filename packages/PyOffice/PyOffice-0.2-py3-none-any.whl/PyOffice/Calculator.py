from .Suite import Suite

class CalculatorProcessor(Suite):
	def __init__(self, process_id):
		self.process_id = process_id

	def add(self, x, y):
		return x + y

	def multiply(self, x, y):
		return x * y

	def divide(self, x, y):
		if y == 0:
			raise ValueError('cannot divide by zero')
		return x / float(y)

	@property 
	def check_process(self):
		'''
		@property decorator turns check_process() into a dynamic 
		attribute - think of this as a java getter().

		to access this method, treat it as an attribute and do 
		>>> myCalc.check_process

		and not
		>>> myCalc.check_process()
		'''
		print(self.process_id)