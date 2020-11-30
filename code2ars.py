#! /usr/bin/python3
# -*- coding: UTF-8 -*-

from importlib import reload
import ast, sys, trace, signal
from multiprocessing import Process, Queue

###### PARAMETERS #####

MAX_LENGTH_TRACE = 1000     # Nb. max. of tokens consiedered for each testcase (usefull in case of infinite loops)

#######################

def initializeParameters(node, symbolDic):
	i=1
	for elem in node.args:
		if elem.arg not in symbolDic.keys():
			symbolDic[elem.arg]='param'+str(i)
			i+=1

def generateNewVarSymbol(symbolDic):
	l = ''.join(symbolDic.values())
	return 'var'+str(l.count('var')+1)

def symbolTranslate(id, symbolDic):
	if id not in symbolDic.keys():
		symbolDic[id] = generateNewVarSymbol(symbolDic)
	return symbolDic[id]

def nodeList2ars(l, symbolDic):
	"""iterate on a list of nodes to translate on a sequence of nodes"""
	res = ''
	for elem in l:
		res += node2ars(elem, symbolDic)+' '
	return res[:(-1)]

UnprocessedNodes = [
	'FunctionDef',
	'Lt',
	'Eq',
	'Gt',
	'GtE',
	'LtE',
	'NotEq',
	'In','NotIn',
	'NoneType',]

def node2ars(node, symbolDic):
	"""translate a python statement into an ARS symbol (level 2)"""

	#NODE : Constant-------------------------------------------------
	if isinstance(node, ast.Constant):
		#return str(node.value)
		return 'Constant_'+node.value.__class__.__name__

	#NODE : Name-----------------------------------------------------
	elif isinstance(node, ast.Name):
		return symbolTranslate(node.id,symbolDic)

	#NODE : Attribute------------------------------------------------
	elif isinstance(node, ast.Attribute):
		return node.attr

	#NODE : Subscript------------------------------------------------
	elif isinstance(node, ast.Subscript):
		return node.__class__.__name__+' '+node2ars(node.value,symbolDic)

	#NODE : BoolOp---------------------------------------------------
	elif isinstance(node, ast.BoolOp):
		return node.__class__.__name__+node.op.__class__.__name__+' '+nodeList2ars(node.values,symbolDic)

	#NODE : BinOp----------------------------------------------------
	elif isinstance(node, ast.BinOp):
		return node.__class__.__name__+node.op.__class__.__name__+' '+node2ars(node.left,symbolDic)+' '+node2ars(node.right,symbolDic)

	#NODE : UnaryOp--------------------------------------------------
	elif isinstance(node, ast.UnaryOp):
		return node.__class__.__name__+node.op.__class__.__name__+' '+node2ars(node.operand,symbolDic)

	#NODE : Assign---------------------------------------------------
	elif isinstance(node,ast.Assign):
		if len(node.targets) > 1 :
			print('WARNING : Assignment with a targets attribut of size greater than 1... is not considered!!')
		if isinstance(node.targets[0],ast.Tuple) :
			ars = ''
			for elem,val in zip(node.targets[0].elts,node.value.elts):
				ars += node.__class__.__name__+' '+node2ars(elem,symbolDic)+' '+node2ars(val,symbolDic)+' '
			return ars
		else :
			return node.__class__.__name__+' '+node2ars(node.targets[0],symbolDic)+' '+node2ars(node.value,symbolDic)

	#NODE : AugAssign------------------------------------------------
	elif isinstance(node,ast.AugAssign):
		return node.__class__.__name__+node.op.__class__.__name__+' '+node2ars(node.target,symbolDic)+' '+node2ars(node.value,symbolDic)

	#NODE : For, AsyncFor--------------------------------------------
	elif isinstance(node,ast.For) or isinstance(node,ast.AsyncFor):
		return node.__class__.__name__+' '+node2ars(node.target,symbolDic)+' '+node2ars(node.iter,symbolDic)

	#NODE : Compare--------------------------------------------------
	elif isinstance(node,ast.Compare):
		res = node.__class__.__name__+' '+node2ars(node.left,symbolDic)
		for i in range(len(node.ops)):
			res += ' '+node2ars(node.ops[i],symbolDic)+' '+node2ars(node.comparators[i],symbolDic)
		return res

	#NODE : Call-----------------------------------------------------
	elif isinstance(node,ast.Call):
		return node.__class__.__name__+'_'+node2ars(node.func,symbolDic)+' '+nodeList2ars(node.args,symbolDic)

	#NODE : List, Tuple----------------------------------------------
	elif isinstance(node,ast.List) or isinstance(node,ast.Tuple):
		if len(node.elts)==0:
			return 'Empty'+node.__class__.__name__
		else:
			return 'NonEmpty'+node.__class__.__name__

	#NODE : While, If------------------------------------------------
	elif isinstance(node,ast.While) or isinstance(node,ast.If):
		return node.__class__.__name__+' '+node2ars(node.test,symbolDic)

	#NODE : Import---------------------------------------------------
	elif isinstance(node,ast.Import):
		return node.__class__.__name__+' '+nodeList2ars(node.names,symbolDic)

	#NODE : ImportFrom-----------------------------------------------
	elif isinstance(node,ast.ImportFrom):
		return node.__class__.__name__+' '+node2ars(node.module,symbolDic)+' '+nodeList2ars(node.names,symbolDic)

	#NODE : alias-----------------------------------------------
	elif isinstance(node,ast.alias):
		return node.__class__.__name__+' '+node2ars(node.name,symbolDic)

	#NODE : Assert---------------------------------------------------
	elif isinstance(node,ast.Assert):
		return ''

	#NODE : Expr-----------------------------------------------------
	elif isinstance(node,ast.Expr):
		return node.__class__.__name__+' '+node2ars(node.value,symbolDic)

	#NODE : Return---------------------------------------------------
	elif isinstance(node,ast.Return):
		return node.__class__.__name__+' '+node2ars(node.value,symbolDic)

	#other nodes
	else :
		if node.__class__.__name__ not in UnprocessedNodes:
			val = ''
			#val=node2ars(node.value,symbolDic) if node.__class__.__name__=='str' else ''
			print("WARNING : node",node.__class__.__name__,": default process",val)
		return node.__class__.__name__

def node2arsLevel1(node, symbolDic):
	"""translate a python statement into an ARS symbol (level 1)"""

	#NODE : Constant-------------------------------------------------
	if isinstance(node, ast.Constant):
		#return str(node.value)
		return 'Constant_'+node.value.__class__.__name__

	#NODE : Name-----------------------------------------------------
	elif isinstance(node, ast.Name):
		return symbolTranslate(node.id,symbolDic)

	#NODE : Subscript------------------------------------------------
	elif isinstance(node, ast.Subscript):
		return node.__class__.__name__+' '+node2arsLevel1(node.value,symbolDic)

	#NODE : BinOp, BoolOp--------------------------------------------
	elif isinstance(node, ast.BinOp) or isinstance(node, ast.BoolOp):
		return node.__class__.__name__+node.op.__class__.__name__

	#NODE : Assign---------------------------------------------------
	elif isinstance(node,ast.Assign):
		if len(node.targets) > 1 :
			print('WARNING : Assignment with a targets attribut of size greater than 1... is not considered!!')
		if isinstance(node.targets[0],ast.Tuple) :
			ars = ''
			for elem,val in zip(node.targets[0].elts,node.value.elts):
				ars += node.__class__.__name__+' '+node2arsLevel1(elem,symbolDic)+' '+node2arsLevel1(val,symbolDic)+' '
			return ars
		else :
			return node.__class__.__name__+' '+node2arsLevel1(node.targets[0],symbolDic)+' '+node2arsLevel1(node.value,symbolDic)

	#NODE : AugAssign------------------------------------------------
	elif isinstance(node,ast.AugAssign):
		return node.__class__.__name__+' '+node2arsLevel1(node.target,symbolDic)+' '+node2arsLevel1(node.value,symbolDic)

	#NODE : While, If----------------------------------------------------
	elif isinstance(node,ast.While) or isinstance(node,ast.If):
		return node.__class__.__name__+' '+node2arsLevel1(node.test,symbolDic)

	#NODE : Return-------------------------------------------------------
	elif isinstance(node,ast.Return):
		return node.__class__.__name__+' '+node2arsLevel1(node.value,symbolDic)

	#other nodes
	else :
		return node.__class__.__name__

def node2arsLevel0(node, symbolDic):
	"""translate a python statement into an ARS symbol (level 0)"""
	return node.__class__.__name__

def node2lineStatement(node, lineDic, symbolDic, arslevel=2):
	"""consider the node and add the line statement to the dictionnary (lineDic)"""
	if isinstance(node, ast.AST):
		if 'lineno' in node._attributes:
			line = str(node.lineno)
			if line not in lineDic.keys():
				#ARS detailed=============================================================
				if isinstance(node,ast.FunctionDef): #initialization of the param symbols
					initializeParameters(node.args, symbolDic)
				if arslevel==2:
					lineDic[line] = node2ars(node, symbolDic)
				elif arslevel==1:
					lineDic[line] = node2arsLevel1(node, symbolDic)
				else :
					lineDic[line] = node2arsLevel0(node, symbolDic)

def ast2lineStatements(node, lineDic, symbolDic, level=0, arslevel=2):
	"""walk the AST and extract the main statement corresponding to each line of the source code"""
	if level==0:
		symbolDic = {'print':'print', 'len':'len', 'range':'range', 'min':'min', 'max':'max'}
	node2lineStatement(node, lineDic, symbolDic,arslevel)
	for field, value in ast.iter_fields(node):
		if isinstance(value, list):
			for item in value:
				if isinstance(item, ast.AST):
					ast2lineStatements(item, lineDic, symbolDic, level=level+1,arslevel=arslevel)
		elif isinstance(value, ast.AST):
			ast2lineStatements(value, lineDic, symbolDic, level=level+1,arslevel=arslevel)
	return lineDic

def str2file(s, filename):
	"""writes the string s in a new file filename"""
	fic = open(filename,'w')
	fic.write(s)
	fic.close()

def handler(signum, frame):
	"""Function used for timeout management during test function"""
	raise Exception("infinite loop")

def getLineFile(n, filename):
	with open(filename, 'r') as file2:
		i=1
		for line in file2:
			if i==n : return line
			i += 1

# Final functions =================================================================================

def Code2Ars(attempt, exercises, arslevel=2, field='exercise_name'):
    """ Returns the Abstract Running Sequence (ARS) from an attempt :
    - attempt   : the learner attempt that contains (at least) the script ('upload' key)
    - exercises : the (dictionary of) exercises )that contain (at least) the testcases ('entries' key) and the name of the functions to test ('funcname' key) on which the attempt has to be executed
    - arslevel  : (default 2) the level of abstraction of the ARS to generate (values 0,1,2 from the least to the most detailed)
    - field     : the field (key) in the attempt that contains the id of the exercise to seek in the *exercises* dictionary
    """

    # identifies the corresponding exercise =======================================================
    try :
        exercise = exercises[attempt[field]]
    except:
        print('Warning : the exercise corresponding to the attempt is not defined in *exercises*')
        return ''

    # store the attempt's script in a separate file ===============================================
    str2file(attempt['upload'],'utils/attemptToTest.py')

    # loads the attempt, generates and analyzes the Abstract Syntactic Tree (AST) =================
    try :
        sys.stdin = open('utils/input.txt')
        import utils.attemptToTest
        reload(utils.attemptToTest)
        astree = ast.parse(attempt['upload'])
        lineStatements = ast2lineStatements(node=astree,lineDic=dict(), symbolDic=dict(),arslevel=arslevel)
        sys.stdin = sys.__stdin__
    except :
        sys.stdin = sys.__stdin__
        return ''

    # generates the Abstract Running Sequence on testcases ========================================
    ars = ''
    origin_out = sys.stdout
    for entry in exercise['entries']:
        # generate the trace for the entry ====================================
        param = str(entry)
        if isinstance(entry, str):
            param = "'"+str(entry)+"'"
        elif isinstance(entry, tuple):
            param = param[1:(len(param)-1)]
        call = 'utils.attemptToTest.'+str(exercise['funcname'])+','+param
        tracer = trace.Trace(count=False, trace=True)	#trace parameters
        signal.signal(signal.SIGALRM, handler)	    #for timeout management
        signal.alarm(1)							    #for timeout management --> 1 sec. <--
        error1 = ''
        try :
            with open('utils/traces.dat', 'w') as filetrace:
                sys.stdout = filetrace
                eval('tracer.runfunc('+call+')')
            sys.stdout = origin_out
        except Exception as exc:
            sys.stdout = origin_out
            error1 = str(exc.__class__)[8:-2]
            error2 = str(exc).replace(' ','_')
            if error2 == 'infinite_loop':
                error1 = error2
        sys.stdout = origin_out
        signal.alarm(0)

        # analyzes the trace for the entry ====================================
        with open('utils/traces.dat', 'r') as filetrace:
            firstLine = True
            nb_symbols = 0
            for line in filetrace:
                if nb_symbols == MAX_LENGTH_TRACE : break
                if firstLine :
                    firstLine = False
                elif 'attemptToTest.py(' in line :
                    lineno = line.replace(')','(').split('(')[1]
                    if lineno not in lineStatements.keys():
                        statement = getLineFile(int(lineno),'utils/attemptToTest.py')
                        if statement != None :
                            print('## WARNING ## trace statement not found in the AST (',statement[:-1],") and replaced by default by 'Else' insid the ARS",nb_symbols)
                            ars += 'Else'+' '
                        else :
                            print("## WARNING ## trace statement not found in the AST and unexisting line (",int(lineno),") in the attempToTest file --> ignore")
                    else:
                        if nb_symbols < MAX_LENGTH_TRACE :
                            ars += lineStatements[lineno]+' '
                    nb_symbols += 1
            ars +=  error1+' '# add the execution error if there is
    return ars    

