import unittest
from PyOffice import CalculatorProcessor, WordProcessor

class PyOfficeTest(unittest.TestCase):

	def setUp(self):
		# self is an unittest object that contains an calculator object
		# ie calculatorprocessor object is stored in unittest object's "my_calc" field
		self.my_calc = CalculatorProcessor(1)
		self.my_processor = WordProcessor(1)

	def test_addition(self):
		assert self.my_calc.add(4,5) == 9
	
	def test_multplication(self):
		assert self.my_calc.multiply(4,5) == 20

	def test_division(self):
		assert self.my_calc.divide(10, 2) == 5

		# https://stackoverflow.com/questions/25047256/assertraises-in-python-unit-test-not-catching-the-exception
		self.assertRaises(ValueError, self.my_calc.divide, 10, 0)

	def test_stringlen(self):
		assert self.my_processor.check_length("hello") == 5
		

if __name__ == "__main__":
    unittest.main()