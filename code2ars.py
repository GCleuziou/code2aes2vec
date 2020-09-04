#! /usr/bin/python3
# -*- coding: UTF-8 -*-

from importlib import reload, import_module
import signal, trace, os, csv, fnmatch, sys
import ast
from ast2ars import ast2str, ast2lineStatements

PATH = 'datasets/Solutions'			# folder into which the exercises' solutions and entries are definied
MAX_LENGTH_TRACE = 1000 	# (in number of symbols) too long traces will be shortened (to deal with infinite loop)

def str2file(s, filename):
	"""write the string s in a new file filename"""
	fic = open(filename,'w')
	fic.write(s)
	fic.close()
def find(pattern, path):
	"""find a file in a tree of files"""
	for root, dirs, files in os.walk(path):
		for name in files:
			if fnmatch.fnmatch(name.lower(), pattern.lower()):
				return os.path.join(root, name)
	return None
def handler(signum, frame):
	"""Function used for timeout management during test function"""
	raise Exception("infinite loop")

class Attempt:
	"""Class defining a learner's attempt (a program/code)"""

	def display(self, detailed = False, i=1):
		"""Displays the attempt"""
		print('Attempt',i,'\t',self.date,'\t',self.learnerID)
		if detailed :
			print(self.code)
			print(self.astree)
			print('Runnability ->',self.runnable)

	def analysis(self):
		"""test the attempt on all entries of the exercise"""
		#write the code of the attempt in a seperate file attempToTest.py
		str2file(self.code, 'attemptToTest.py')
		#try to import the File
		try :
			import attemptToTest
			reload(attemptToTest)
			self.importable = True
			#extract the line statements from the AST
			self.lineStatements = ast2lineStatements(ast.parse(self.code),lineDic=dict(), symbolDic=dict())
		except :
			self.importable = False
			return None

		#try to run the file on entries and build traces
		origin_out = sys.stdout
		i = 0
		for entry in self.exercise.entries:
			#entry preparation
			param = str(entry)
			if isinstance(entry, str):
				param = "'"+str(entry)+"'"
			elif isinstance(entry, tuple):
				param = param[1:(len(param)-1)]

			call = 'attemptToTest.'+str(self.exercise.name)+','+param
			print('<->',call)
			tracer = trace.Trace(count=False, trace=True)	#trace parameters
			signal.signal(signal.SIGALRM, handler)	#for timeout management
			signal.alarm(1)							#for timeout management --> 1 sec. <--
			try :
				with open('traces.dat', 'w') as filetrace:
					sys.stdout = filetrace
					eval('tracer.runfunc('+call+')')
				sys.stdout = origin_out
				self.runnable.append(True)
				self.errors.append('')
			except Exception as exc:
				sys.stdout = origin_out
				self.runnable.append(False)
				error1 = str(exc.__class__)[8:-2]
				error2 = str(exc).replace(' ','_')
				print('=============================>',error1,error2)
				if error2 == 'infinite_loop':
					error1 = error2
				self.errors.append(error1)
			sys.stdout = origin_out
			signal.alarm(0)
			#trace analysis----------------
			ars = ''   # Abstract Running Sequence (ARS)
			with open('traces.dat', 'r') as filetrace:
					firstLine = True
					nb_symbols = 0
					for line in filetrace:
						if firstLine :
							firstLine = False
						elif 'attemptToTest.py(' in line :
							lineno = line.replace(')','(').split('(')[1]
							if lineno not in self.lineStatements.keys():
								statement = getLineFile(int(lineno),'attemptToTest.py')
								if statement != None :
									print('## WARNING ## trace statement not found in the AST (',statement[:-1],") and replaced by default by 'Else' inside the ARS")
									ars += 'Else'+' '
								else :
									print("## WARNING ## trace statement not found in the AST and unexisting line (",int(lineno),") in the attempToTest file --> ignore")

							else:
								if nb_symbols < MAX_LENGTH_TRACE :
									ars += self.lineStatements[lineno]+' '
								nb_symbols += 1
			self.traces.append(ars+self.errors[i]) # add the execution error if there is
			i += 1

	def __init__(self, code, date, learnerID, success, exercise):
		self.code = code
		self.date = date
		self.learnerID = learnerID
		self.exercise = exercise
		self.importable = None			#default value
		try:
			self.astree=ast.parse(self.code)
		except:
			self.astree=None
		self.runnable = []				#default value
		self.errors = []				#default value
		self.lineStatements = None
		self.traces = []
		self.success = int(success)

class Exercise: 
	"""Class defining an exercise with the corresponding attempts"""

	def display(self, detailed = False):
		"""Displays the exercise"""
		print("Exercise ",self.name," (",self.ID,") ----------",sep='')
		if detailed :
			i = 1
			for a in self.attempts:
				a.display(False, i)
				i += 1
		else :
			print('   ',len(self.attempts),'attempts')
			print('      ',self.nbImportable(),'importable')
			print('      ',self.nbAstreable(),'AST generated')
			print('      ',self.nbFullyRunnable(),'fully runnable')
			print('      ',self.nbPartiallyRunnable(),'partially runnable')
            
	def loadAttempts(self, csvfilename, reset=True):
		"""seek the corresponding attempts in the csv file and load them in the exercise
		parameter 'reset' indicates wether the list of attempts has to be removed before loading"""
		if reset :
			self.attempts = []
		with open(csvfilename) as csvfile:
			csv_reader = csv.reader(csvfile, delimiter = ',')
			numLine = 0
			for line in csv_reader:
				if numLine>0:	#skip the header line in the csv file
					if line[6]==self.ID:
						a = Attempt(line[3], line[2], line[4], line[1], self)
						self.attempts.append(a)
				numLine += 1

	def loadEntries(self, moduleName):
		"""seek the visible/unvisible entries in the solution file and load them in the exercise"""
		#seek the module in the file system
		#print("Recherche ->",moduleName)
		res=find(moduleName+'.py',PATH)
		try:
			res=res.split('/')
		except:
			print("Definition of exercise '",moduleName,"' not found",sep='')
			return None
		res[-1]=res[-1][:len(res[-1])-3]
		res='.'.join(res)
		#print(moduleName,res)
		#import the module
		moduleSol = import_module(res)
		moduleSol = reload(moduleSol)
		self.entries = eval('moduleSol.entrees_visibles')
		self.entries += eval('moduleSol.entrees_invisibles')

	def nbImportable(self):
		"""Computes the number of importable attempts among the list of attempts for this exercise"""
		n=0
		for a in self.attempts:
			n += 1 if a.importable else 0
		return n
	def nbPartiallyRunnable(self):
		"""Computes the number of partially runnable attempts among the list of attempts for this exercise"""
		n=0
		for a in self.attempts:
			n += 1 if any(a.runnable) and not all(a.runnable) else 0
		return n
	def nbFullyRunnable(self):
		"""Computes the number of fully runnable attempts among the list of attempts for this exercise"""
		n=0
		for a in self.attempts:
			n += 1 if all(a.runnable)==True else 0
		return n
	def nbAstreable(self):
		"""Computes the number of attempts that can be converted into ASTree"""
		n=0
		for a in self.attempts:
			n += 1 if a.astree else 0
		return n

	def analysis(self):
		"""analyze each attemps from exercise"""
		for att in self.attempts:
			att.analysis()

	def __init__(self, exerciseID, exerciseName):
		self.ID = exerciseID
		self.name = exerciseName
		self.attempts = []	# contains the learner's attempts for this exercise
		self.entries = None	# contains the list of 'unit' tests that evaluates the attempts
		self.loadEntries(self.name)

class Dataset: 
	"""Class defining a (PCAP) dataset as a dictionnary of exercises"""

	def display(self, detailed = False):
		"""Displays the dataset"""
		for e in self.dataset.values():
			e.display(detailed)
	
	def pcapfile2data(self, csvfilename, filter=[]):
		"""This function parse the (csv) pcapfile and build a dictionary of exercises with corresponding attempts"""
		data=dict()

		#build the dictionnary of exercises (without attempts)
		with open(csvfilename) as csvfile:
			csv_reader = csv.reader(csvfile, delimiter = ',')
			numLine = 0
			for line in csv_reader:
				if numLine>0:	#skip the header line in the csv file
					if line[6] not in data.keys() and (line[6] in filter or filter==[]):
						data[line[6]] = Exercise(line[6], line[5])
				numLine += 1
		#load the attempts
		for e in data.values():
			e.loadAttempts(csvfilename, reset = True)
		self.dataset = data

	def analysis(self):
		"""analyze each attemps from each exercise"""
		for  e in self.dataset.values():
			e.analysis()

	def __init__(self, csvfilename, filter=[]):
		self.dataset = dict()
		self.pcapfile2data(csvfilename, filter)

def dataset2corpus(data,filename,selection=None):
	"""build a corpus of 'ARS' from the entire dataset :
	each attempts with non-empty trace leads to a (one line) ARS"""
	with open(filename, 'w') as filecorpus :
		for exo in data.dataset.values():
			if selection == None or exo.ID in selection:
				for att in exo.attempts :
					if len(att.traces)>0:
						filecorpus.write(' '.join(att.traces)+'\n')
					else :
						filecorpus.write('\n')


