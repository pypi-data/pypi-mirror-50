import os

class listFiles:
	
	#Accepts 4 parameters, return list
	
	#filePath, fileExtension, fileReturn, filecountVerbose
	
	#	fileReturn - values
	#	0 - return root, dirs, filename
	#	1 - return root only
	#	2 - return dirs only
	#	3 - return filename only(default)
	#	4 - return root and filename
	# 	5 - return root and filename without extension
	
	#	filecountVerbose = 1 will print number of files found
	
	#CONSTRUCTOR#
	#def __init__(self, filePath, fileExtension, fileReturn=3, filecountVerbose=0):
	#	self.filePath = filePath
	#	self.fileExtension = fileExtension
	#	self.fileReturn = fileReturn
	#	self.filecountVerbose = filecountVerbose
		
	def iterateFiles(self, filePath, fileExtension, fileReturn, filecountVerbose):
		
		#checking if dot will get the current directory
		if filePath == '.':
			filePath = os.getcwd()
		
		if int(fileReturn) > 5:
			print('''Invalid third parameter\n
0 - return root, dirs, filename
1 - return root only
2 - return dirs only
3 - return filename only
4 - return root and filename
			''')
			exit()
		
		if os.path.exists(filePath):
			storeFile = []
			countFiles = 0
			for root, dirs, files in os.walk(filePath):
				for filename in files:
					if filename.lower().endswith(fileExtension):
						temp = []
						if int(fileReturn) == 0:
							temp.append(root)
							temp.append(dirs)
							temp.append(filename)
							storeFile.append(temp)
						elif int(fileReturn) == 1:
							storeFile.append(root)
						elif int(fileReturn) == 2:
							storeFile.append(dirs)
						elif int(fileReturn) == 3:
							storeFile.append(filename)
						elif int(fileReturn) == 4:
							temp.append(root)
							temp.append(filename)
							storeFile.append(temp)
						countFiles += 1
			
			if filecountVerbose == 1:
				print("Total number of files found: " + str(countFiles))
			return storeFile
			
		else:
			print("Path doesn't exists!")
			exit()
	
