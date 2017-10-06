import os

class Search:
	def __init__(self, dirList):
		self.results = []

		self.erroredFiles = []

		self.blackList = []
		self.whiteList = []

		self.directoriesToSearch = dirList

		self._filesScanned = 0

	def searchForFileName(self, name):
		self.clearResults()
		for searchDir in self.directoriesToSearch:
			for root, dirs, files in os.walk(searchDir):
				for file in files:
					self._filesScanned = self._filesScanned+1
					inBlackList = False
					inWhiteList = False
					if name in file:
						if self.blackList != []:
							for bli in self.blackList:
								if file.endswith(bli):
									inBlackList = True
									continue

						if self.whiteList != []:
							for wli in self.whiteList:
								if file.endswith(wli):
									inWhiteList = True
									continue

						if (inBlackList == False) and (self.blackList != []):
							#If file not flagged in black list, and black list is set, then add result
							self._AddResult(file, root)
						elif (inWhiteList == True) and (self.whiteList != []):
							#If file flagged in white list, and white list is set, then add result
							self._AddResult(file, root)
						elif (self.whiteList == []) and (self.blackList == []):
							#If neither list is set, then add to result
							self._AddResult(file, root)
						else:
							continue
		return self.results

	def searchForStringInFile(self, string):
		self.clearResults()
		for searchDir in self.directoriesToSearch:
			for root, dirs, files in os.walk(searchDir):
				for file in files:
					self._filesScanned = self._filesScanned+1
					inBlackList = False
					inWhiteList = False
					if self.blackList != []:
						for bli in self.blackList:
							if file.endswith(bli):
								inBlackList = True
								continue

					if self.whiteList != []:
						for wli in self.whiteList:
							if file.endswith(wli):
								inWhiteList = True
								continue

					if (inBlackList == False) and (self.blackList != []):
						#If file not flagged in black list, and black list is set, then add result
						self._ReadThroughForString(root, file, string)
					elif (inWhiteList == True) and (self.whiteList != []):
						#If file flagged in white list, and white list is set, then add result
						self._ReadThroughForString(root, file, string)
					elif (self.whiteList == []) and (self.blackList == []):
						#If neither list is set, then add to result
						self._ReadThroughForString(root, file, string)
					else:
						continue
		return self.results

	def getFileListResults(self):
		l = []
		for item in self.results:
			l.append(item.fullFileName)
		return l

	def setExtensionBlacklist(self, list):
		if self.whiteList != []:
			raise Exception("You cannot use a whitelist and blacklist at the same time")
		self.blacklist = list

	def setExtensionWhiteList(self, list):
		if self.blackList != []:
			raise Exception("You cannot use a whitelist and blacklist at the same time")
		self.whiteList = list

	def clearResults(self):
		self._filesScanned = 0
		self.results = []

	def _AddResult(self, file, root):
		result = Result(file, root)
		self.results.append(result)
		return result

	def _ReadThroughForString(self, root, file, string, encoding="utf-8"):
		try:
			with open(os.path.join(root, file), "r", 1024) as f:
				i = 0
				for line in f:
					if string in line:
						self._AddResult(file, root).matchingLines[i] = line
					i = i+1
		except IOError:
			self.erroredFiles.append(os.path.join(root, file))

class Result:
	def __init__(self, name, location):
		self.fileName = name
		self.fileLocation = location
		self.fullFileName = os.path.join(location, name)

		self.matchingLines = {} #Number:Line

	def __str__(self):
		try:
			abbreviatedName = self.fullFileName.split("\\")
			abbreviatedName = abbreviatedName[1] + "/.../" + abbreviatedName[len(abbreviatedName)-2]+"/"+abbreviatedName[len(abbreviatedName)-1]
		except:
			abbreviatedName = self.fullFileName.split("/")
			abbreviatedName = abbreviatedName[1] + "/.../" + abbreviatedName[len(abbreviatedName)-2]+"/"+abbreviatedName[len(abbreviatedName)-1]
		return("Result (File: %s) (Matching Lines: %i)"%(abbreviatedName, len(self.matchingLines)))

#if __name__ == "__main__":
#	s = Search([r"C:\Riot Games"])
#	s.SetExtensionWhiteList([".mp4", ".bnk"])
#	results = s.SearchForFileName("")
#	for res in results:
#		print(res.fullFileName)
