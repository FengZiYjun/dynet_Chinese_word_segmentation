
class Logger:
	def __init__(self, w_file):
		self.file = w_file

	def log(self, meg):
		with open(self.file, "w") as f:
			f.write(meg.encode('utf8'))
	
