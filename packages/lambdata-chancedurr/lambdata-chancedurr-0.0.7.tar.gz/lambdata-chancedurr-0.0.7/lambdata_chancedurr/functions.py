
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
