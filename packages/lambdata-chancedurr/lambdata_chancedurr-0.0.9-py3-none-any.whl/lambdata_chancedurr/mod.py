def checkNulls(dataframe):
	df = dataframe
	nulls = df.isnull().sum()
	for col, null in nulls.items():
		print(f'\'{col}\' has {null} null value(s).')

def addListToDataframe(alist, dataframe, colName = 'new_column'):
	import pandas as pd
	newCol = pd.DataFrame(alist, columns=[colName])
	dataframe = dataframe.join(newCol)
	return dataframe

class Shirt():

	def __init__(self, style, sleeve, size, material):
		self.style = style
		self.sleeve = sleeve
		self.size = size 
		self.material = material

	def description(self):
		print(
			f('Style: {self.style}'),
			f('Size: {self.size}'),
			f('Material: {self.material}'),
			f('Sleeve: {self.sleeve}')
		)