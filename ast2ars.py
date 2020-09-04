#! /usr/bin/python3
# -*- coding: UTF-8 -*-

import ast

def ast2str(node, level=0):
	"""
	transforme un AST en une chaîne de caractère tel que attendu par apted
	"""
	#print('  ' * level + str_node(node))
	chaine='{'+str_node(node)
	for field, value in ast.iter_fields(node):
		if isinstance(value, list):
			for item in value:
				if isinstance(item, ast.AST):
					chaine+=ast2str(item, level=level+1)
		elif isinstance(value, ast.AST):
			chaine+=ast2str(value, level=level+1)
	chaine+='}'
	return chaine

def initializeParameters(node, symbolDic):
	i=1
	#symbolDic = dict()
	for elem in node.args:
		#print(elem.arg)
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

def node2ars(node, symbolDic):
	"""translate a python statement into an ARS (ex. Assignment(x=3) --> Assign var1 3)"""

	#NODE : Constant-------------------------------------------------
	if isinstance(node, ast.Constant):
		#return str(node.value)
		return 'Constant_'+node.value.__class__.__name__

	#NODE : Name-----------------------------------------------------
	elif isinstance(node, ast.Name):
		return symbolTranslate(node.id,symbolDic)

	#NODE : Subscript------------------------------------------------
	elif isinstance(node, ast.Subscript):
		return node.__class__.__name__+' '+node2ars(node.value,symbolDic)

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
				ars += node.__class__.__name__+' '+node2ars(elem,symbolDic)+' '+node2ars(val,symbolDic)+' '
			return ars
		else :
			return node.__class__.__name__+' '+node2ars(node.targets[0],symbolDic)+' '+node2ars(node.value,symbolDic)

	#NODE : AugAssign------------------------------------------------
	elif isinstance(node,ast.AugAssign):
		return node.__class__.__name__+' '+node2ars(node.target,symbolDic)+' '+node2ars(node.value,symbolDic)

	#NODE : While, If----------------------------------------------------
	elif isinstance(node,ast.While) or isinstance(node,ast.If):
		return node.__class__.__name__+' '+node2ars(node.test,symbolDic)

	#NODE : Return-------------------------------------------------------
	elif isinstance(node,ast.Return):
		return node.__class__.__name__+' '+node2ars(node.value,symbolDic)

	#other nodes
	else :
		return node.__class__.__name__

def node2lineStatement(node, lineDic, symbolDic):
	"""consider the node and add the line statement to the dictionnary (lineDic)"""
	if isinstance(node, ast.AST):
		if 'lineno' in node._attributes:
			line = str(node.lineno)
			if line not in lineDic.keys():
				#ARS detailed=============================================================
				if isinstance(node,ast.FunctionDef): #initialization of the param symbols
					initializeParameters(node.args, symbolDic)
				lineDic[line] = node2ars(node, symbolDic)
				#print(lineDic[line])

def ast2lineStatements(node, lineDic, symbolDic, level=0):
	"""walk the AST and extract the main statement corresponding to each line of the source code"""
	node2lineStatement(node, lineDic, symbolDic)
	for field, value in ast.iter_fields(node):
		if isinstance(value, list):
			for item in value:
				if isinstance(item, ast.AST):
					ast2lineStatements(item, lineDic, symbolDic, level=level+1)
		elif isinstance(value, ast.AST):
			ast2lineStatements(value, lineDic, symbolDic, level=level+1)
	return lineDic
