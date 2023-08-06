from fileOperations import listFiles

def fileSearch(filePath, fileExtension, fileReturn=3, filecountVerbose=0):
	
	listFileObject = listFiles()
	return listFileObject.iterateFiles(filePath,fileExtension,fileReturn,filecountVerbose)
