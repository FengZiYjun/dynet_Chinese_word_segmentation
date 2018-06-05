
class Logger:
	def __init__(self, w_file):
		self.file = w_file

	def log(self, meg):
		with open(self.file, "w", encoding="utf-8") as f:
			f.write(meg)
	
