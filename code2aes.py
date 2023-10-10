import sys
import ast
import builtins

class BoucleInfinie(Exception):
    pass

class Tracer():

    def __init__(self):
        """
            lines_trace = liste contenant les lignes executees lors de l'appel d'une fonction
            nb_max_entree = taille maximale de la liste de lines_trace avant de detecter une condition de boucle infini
            list_event = liste des events a recuperer
        """
        self.lines_trace = []
        self.nb_max_entree = 400
        # call, line, return, exception, opcode
        self.list_event = ["call", "line"]

    def tracer(self, frame, event, arg = None):
        """
            Definit la methode de trace
        """
        line_no = frame.f_lineno
        if(len(self.lines_trace)>self.nb_max_entree):
            raise BoucleInfinie()
        if event in self.list_event:
            #print(f"A {event} at line number {line_no} ")
            self.lines_trace.append(line_no)
        return self.tracer

    def get_trace_and_result(self,fonction,*args,**kwargs):
        """
            Execute une fonction pour en extraire la trace d'execution.

            @param fonction: le nom de la fonction
            @param args: les arguments de la fonction ( mis un par un )

            @return un tuple trace, contenant la liste des lignes executees ainsi que , et res, le resultat de la fonction
        """
        # mise en place de la fonction trace
        sys.settrace(self.tracer)

        # appel de la fonction a tester
        try:
            res = fonction(*args)
        except BoucleInfinie as e:
            trace = self.lines_trace
            self.lines_trace = []
            sys.settrace(None)
            return(trace, "Boucle infinie", "InfiniteLoop")
        except: # catch *all* exceptions
            trace = self.lines_trace
            self.lines_trace = []
            sys.settrace(None)
            return(trace, str(sys.exc_info()), "TypeError")

        # on recupere la liste des lignes executees pendant la trace
        trace = self.lines_trace
        self.lines_trace = []
        sys.settrace(None)

        return trace,res,""

# Exemple d'appel a Tracer
# t = Tracer()
# print(t.get_trace_and_result(fun,1,2,3))

# Autres methodes pour generer une trace :
# - utiliser le module hunter de python
#       trace_f = []
#       hunter.trace(function="g", action=(lambda x: trace_f.append(x)))
#       print(f(5)) #trace_f contient la liste des lignes executees
# - utiliser le module trace de python
#       tracer = trace.Trace(count=False, trace=True)
#       tracer.run("t.get_trace_and_result(fun,arg)")
#       r = tracer.results()

class ASTnormaliser():
    def __init__(self):
        listSymbolDict = dir(__builtins__)
        self.symbolDic = dict()
        for item in listSymbolDict: 
            self.symbolDic[item]=(item,None)

    def ast2astNormaliserPython(self,ast_base):
        self.functionParent(ast_base)

    def functionParent(self, node, fonction = None):
        """
        applique un attribut "funct" sur chaque noeud d'un ast qui definie la fonction dans laquelle il est defini

        @param node: passer un ast complet a la fonction, celle ci effectura un appel recursif sur l'ensemble de l'arbre
        """
        can_pass = True
        if isinstance(node,ast.FunctionDef):
            fonction = node
            node.funct = node
            self.initializeParameters(node)
        if isinstance(node,ast.ListComp):
            fonction = node
            node.funct = node
        if isinstance(node,ast.Name):
            self.symbolTranslate(node)
        if isinstance(node,ast.Call) and hasattr(node, "args"):
            for name in node.args:
                name.funct = fonction
                self.symbolTranslate(name)
            can_pass=False
        if can_pass:
            for child in ast.iter_child_nodes(node):
                child.funct = fonction
                self.functionParent(child, fonction)

    def initializeParameters(self, node):
        """normalise les parametres d'un node function"""
        keys = self.symbolDic.keys()
        l = ''
        for key in keys:
            l+=str(key)
        i=l.count('param')+1
        for elem in node.args.args:
            self.symbolDic['param'+str(i)]=(elem.arg,node.funct)
            elem.arg = 'param'+str(i)
            i+=1

    def generateNewVarSymbol(self):
        """generation d'un nouveau symbole pour le dictionnaire de symboles"""
        keys = self.symbolDic.keys()
        i = 1
        while( 'var'+str(i) in self.symbolDic):
            i+=1
        return 'var'+str(i)

    def symbolTranslate(self, node):
        """normalise une variable dans un ast"""
        try :
            id = node.id
            var=None
            for key in self.symbolDic:
                values = self.symbolDic[key]
                if values[0]==id:
                    if values[1]==node.funct:
                        var = key
            if var==None:
                var = self.generateNewVarSymbol()
                self.symbolDic[var] = (id,node.funct)
            node.id = var
        except AttributeError:
            pass
            

def code2astPython(
        code
    ):
    """
    Transforme une chaine de caractere de code Python en un abre syntaxique abstrait.

    @param code_etu: une chaine de caracteres contenant le code soumis

    @return l'Arbre Syntaxique Abstrait du code
    """
    astree = ast.parse(code)

    # normalisation de l'ast pour les parametres et variables
    t = ASTnormaliser()
    t.ast2astNormaliserPython(astree)
    return astree
    # avec dump.ast(...) renvoie un objet str plutot qu'un objet <class 'ast.Module'>

def dump_ast(tree):
    return ast.dump(tree)

def ast2codePython(tree):
#reconstruit le code python a partir d'un ast
    import astor
    return astor.to_source(tree)

# Decorateur
def addFunction2AES(classe):
    def deco(fonction):
        classe.toAES=fonction
        return fonction
    return deco

#=========================================================================================
#NODE : alias------------------------------------------------------------------------------------------------------
@addFunction2AES(ast.alias)
def alias2AES(self, node):
    return node.__class__.__name__+' '+node2aes(node.name)
#NODE : Assert, Lambda, Raise------------------------------------------------------------------------------------------------------
@addFunction2AES(ast.Assert)
@addFunction2AES(ast.Lambda)
@addFunction2AES(ast.Raise)
def Assert2AES(self, node):
    return ''
#NODE : Assign----------------------------------------------------------------------------------------------------
@addFunction2AES(ast.Assign)
def Assign2AES(self, node):
    if len(node.targets) > 1 :
        return node.__class__.__name__+' '+nodeList2aes(node.targets)
    if isinstance(node.targets[0],ast.Tuple) :
        aes = ''
        for elem,val in zip(node.targets[0].elts,node.value.elts):
            aes += node.__class__.__name__+' '+node2aes(elem)+' '+node2aes(val)+' '
        return aes
    else :
        return node.__class__.__name__+' '+node2aes(node.targets[0])+' '+node2aes(node.value)
#NODE : AugAssign----------------------------------------------------------------------------------------------------
@addFunction2AES(ast.AugAssign)
def AugAssign2AES(self, node):
    return node.__class__.__name__+node.op.__class__.__name__+' '+node2aes(node.target)+' '+node2aes(node.value)
#NODE : AnnAssign----------------------------------------------------------------------------------------------------
@addFunction2AES(ast.AnnAssign)
def AnnAssign2AES(self, node):
    return node.__class__.__name__+node.annotation.__class__.__name__+' '+node2aes(node.target)
#NODE : Attribute----------------------------------------------------------------------------------------------------
@addFunction2AES(ast.Attribute)
def Attribute2AES(self, node):
    return node.attr
#NODE : BoolOp----------------------------------------------------------------------------------------------------
@addFunction2AES(ast.BoolOp)
def BoolOp2AES(self, node):
    return node.__class__.__name__+node.op.__class__.__name__+' '+nodeList2aes(node.values)
#NODE : BinOp----------------------------------------------------------------------------------------------------
@addFunction2AES(ast.BinOp)
def BinOp2AES(self, node):
    return node.__class__.__name__+node.op.__class__.__name__+' '+node2aes(node.left)+' '+node2aes(node.right)
#NODE : Compare----------------------------------------------------------------------------------------------------
@addFunction2AES(ast.Compare)
def Compare2AES(self, node):
    res = node.__class__.__name__+' '+node2aes(node.left)
    for i in range(len(node.ops)):
        res += ' '+node2aes(node.ops[i])+' '+node2aes(node.comparators[i])
    return res
#NODE : Call----------------------------------------------------------------------------------------------------
@addFunction2AES(ast.Call)
def Call2AES(self, node):
    return node.__class__.__name__+'_'+node2aes(node.func)+' '+nodeList2aes(node.args)
#NODE : Constant----------------------------------------------------------------------------------------------------
@addFunction2AES(ast.Constant)
def Constant2AES(self, node):
    return 'Constant_'+node.value.__class__.__name__
#NODE : ClassDef------------------------------------------------------------------------------------------------------
@addFunction2AES(ast.ClassDef)
def ClassDef2AES(self, node):
    return 'ClassDef_'+node.__class__.__name__
#NODE : Dict----------------------------------------------------------------------------------------------------
@addFunction2AES(ast.Dict)
def Dict2AES(self, node):
    if len(node.keys)==0:
        return 'Empty'+node.__class__.__name__
    else:
        return 'NonEmpty'+node.__class__.__name__
#NODE : Expr, Yield, YieldFrom------------------------------------------------------------------------------------------------------
@addFunction2AES(ast.Expr)
@addFunction2AES(ast.Yield)
@addFunction2AES(ast.YieldFrom)
def Expr2AES(self, node):
    return node.__class__.__name__+' '+node2aes(node.value)
#NODE : FormattedValue------------------------------------------------------------------------------------------------------
@addFunction2AES(ast.FormattedValue)
def FormattedValue2AES(self, node):
    return 'FormattedValue_'+node.value.__class__.__name__
#NODE : For, AsyncFor----------------------------------------------------------------------------------------------------
@addFunction2AES(ast.For)
@addFunction2AES(ast.AsyncFor)
def For2AES(self, node):
    return node.__class__.__name__+' '+node2aes(node.target)+' '+node2aes(node.iter)
#NODE : Global, Nonlocal----------------------------------------------------------------------------------------------------
@addFunction2AES(ast.Global)
@addFunction2AES(ast.Nonlocal)
def Global2AES(self, node):
    res = node.__class__.__name__+' '+nodeList2aes(node.names)
    for elem in node.names:
        res += elem + ', '
    return res
#NODE : Import------------------------------------------------------------------------------------------------------
@addFunction2AES(ast.Import)
def Import2AES(self, node):
    return node.__class__.__name__+' '+nodeList2aes(node.names)
#NODE : ImportFrom------------------------------------------------------------------------------------------------------
@addFunction2AES(ast.ImportFrom)
def ImportFrom2AES(self, node):
    return node.__class__.__name__+' '+node2aes(node.module)+' '+nodeList2aes(node.names)
#NODE : JoinedStr----------------------------------------------------------------------------------------------------
@addFunction2AES(ast.JoinedStr)
def JoinedStr2AES(self, node):
    return node.__class__.__name__+' '+nodeList2aes(node.values)
#NODE : Delete----------------------------------------------------------------------------------------------------
@addFunction2AES(ast.Delete)
def Delete2AES(self, node):
    return node.__class__.__name__+' '+nodeList2aes(node.targets)
#NODE : List, Tuple, Set----------------------------------------------------------------------------------------------------
@addFunction2AES(ast.List)
@addFunction2AES(ast.Tuple)
@addFunction2AES(ast.Set)
def List2AES(self, node):
    if len(node.elts)==0:
        return 'Empty'+node.__class__.__name__
    else:
        return 'NonEmpty'+node.__class__.__name__
#NODE : Name----------------------------------------------------------------------------------------------------
@addFunction2AES(ast.Name)
def Name2AES(self, node):
    return node.id
#NODE : NamedExpr----------------------------------------------------------------------------------------------------
if hasattr(ast, "NamedExpr"):
    @addFunction2AES(ast.NamedExpr)
    def NamedExpr2AES(self, node):
        return node.__class__.__name__+' '+node2aes(node.target)+' '+node2aes(node.value)
#NODE : Return------------------------------------------------------------------------------------------------------
@addFunction2AES(ast.Return)
def Return2AES(self, node):
    return node.__class__.__name__+' '+node2aes(node.value)
#NODE : Slice----------------------------------------------------------------------------------------------------
@addFunction2AES(ast.Slice)
def Slice2AES(self, node):
    return node.__class__.__name__+' '+node2aes(node.lower)+' '+node2aes(node.upper)
#NODE : Subscript, Starred----------------------------------------------------------------------------------------------------
@addFunction2AES(ast.Subscript)
@addFunction2AES(ast.Starred)
def Subscript2AES(self, node):
    return node.__class__.__name__+' '+node2aes(node.value)
#NODE : Try----------------------------------------------------------------------------------------------------
@addFunction2AES(ast.Try)
def Try2AES(self, node):
    return node.__class__.__name__
#NODE : UnaryOp----------------------------------------------------------------------------------------------------
@addFunction2AES(ast.UnaryOp)
def UnaryOp2AES(self, node):
    return node.__class__.__name__+node.op.__class__.__name__+' '+node2aes(node.operand)
#NODE : While, If, IfExp------------------------------------------------------------------------------------------------------
@addFunction2AES(ast.While)
@addFunction2AES(ast.If)
@addFunction2AES(ast.IfExp)
def If2AES(self, node):
    return node.__class__.__name__+' '+node2aes(node.test)
#NODE : With, AsyncWith------------------------------------------------------------------------------------------------------
@addFunction2AES(ast.With)
@addFunction2AES(ast.AsyncWith)
def With2AES(self, node):
    return node.__class__.__name__+' '+nodeList2aes(node.items)
#NODE : withitem------------------------------------------------------------------------------------------------------
@addFunction2AES(ast.withitem)
def withitem2AES(self, node):
    return node.__class__.__name__+' '+node2aes(node.context_expr)+' '+node2aes(node.optional_vars)
#NODE : ListComp, SetComp, GeneratorExp------------------------------------------------------------------------------------------------------
@addFunction2AES(ast.ListComp)
@addFunction2AES(ast.SetComp)
@addFunction2AES(ast.GeneratorExp)
def ListComp2AES(self, node):
    return node.__class__.__name__+' '+node2aes(node.elt)
#NODE : DictComp------------------------------------------------------------------------------------------------------
@addFunction2AES(ast.DictComp)
def DictComp2AES(self, node):
    return node.__class__.__name__+' '+node2aes(node.key)+' '+node2aes(node.value)
#=========================================================================================

def nodeList2aes(l):
    """iterer sur une liste de noeuds a traduire en une sequence de noeuds"""
    res = ''
    for elem in l:
        res += node2aes(elem)+' '
    return res[:(-1)]

def node2aes(node):
    """traduire une instruction python en un symbole AES (niveau 2)"""
    try:
        return node.toAES(node)
	#other nodes
    except:
        UnprocessedNodes = [
            'FunctionDef',
            'Load',
            'Store',
            'Del',
            'And',
            'Or',
            'Add',
            'Sub',
            'Mult',
            'MatMult',
            'Div',
            'Mod',
            'Pow',
            'LShift',
            'RShift',
            'BitOr',
            'BitXor',
            'BitAnd',
            'FloorDiv',
            'Invert',
            'Not',
            'UAdd',
            'USub',
            'Eq',
            'NotEq',
            'Lt',
            'LtE',
            'Gt',
            'GtE',
            'Is',
            'IsNot',
            'In',
            'NotIn',
            'NoneType',
            'Str',]
        
        if node.__class__.__name__ not in UnprocessedNodes:
            val = ''
            #print("WARNING : node",node.__class__.__name__,": default process",val)
        return node.__class__.__name__

def ast_line_to_dict_item(astree, dic_line = None):
    """
    Creer un dictionnaire d'objet AST a partir d'un AST

    @param astree: un AST

    @return un dictionnaire de noeud ast avec le numero de la ligne en cle et l'objet ast en valeur
    """
    if dic_line == None:
        dic_line = dict()
    for field, value in ast.iter_fields(astree):
        if isinstance(value, list):
            for item in value:
                if isinstance(item, ast.AST) and hasattr(item, 'lineno'):
                    if item.lineno not in dic_line:
                        dic_line[item.lineno] = item
                    ast_line_to_dict_item(item, dic_line)
        elif isinstance(value, ast.AST):
            ast_line_to_dict_item(value, dic_line)
    return dic_line

def dict_item_to_dict_line(dic_aes_items):
    """
    Creer un dictionnaire de phrases pour chacune des lignes de l'AST

    @param dic_aes_items: un dictionnaire de noeud ast avec le numero de la ligne en cle et l'objet ast en valeur

    @return un dictionnaire de phrase aes avec le numero de la ligne en cle et la phrase traduite avec l'aes en valeur
    """
    res = dict()
    for line in dic_aes_items:
        node = dic_aes_items[line]
        res[line] = node2aes(node)
    return res

def astTrace2aes(astree, trace, erreur):
    """
    Creer l'AES grace a l'AST et la trace d'execution

    @param astree: un AST
    @param trace: trace d'execution du code
    @param erreur: l'erreur retourner par la fonction lors de l'execution

    @return l'AES du code execute
    """
    res = ''
    # creer un dictionnaire d'objet AST a partir d'un AST
    dict_item = ast_line_to_dict_item(astree)

    # a partir du dictionnaire d'objet AST, creer un dictionnaire de phrases pour chacune des lignes de l'AST
    dico_phrase = dict_item_to_dict_line(dict_item)
    # redaction de l'aes
    for i in trace:
        try:
            res += dico_phrase[i] + " "
        except KeyError:
            print('Warning : pb. trace')
    if erreur!="":
        res += erreur
    return res

def Code2Aes(attempt, exercises, aeslevel=2, field='exercise_name'):
    """
    Returns the Abstract Running Sequence (AES) from an attempt :
	- attempt   : the learner attempt that contains (at least) the script ('upload' key)
	- exercises : the (dictionary of) exercises that contain (at least) the testcases ('entries' key) and the name of the functions to test ('funcname' key) on which the attempt has to be executed
	- aeslevel  : (default 2) the level of abstraction of the AES to generate (values 0,1,2 from the least to the most detailed
	- field     : the field (key) in the attempt that contains the id of the exercise to seek in the *exercises* dictionary
"""
    from importlib import util
    # identifies the corresponding exercise =======================================================
    try :
        exercise = exercises[attempt[field]]
    except:
        print('Warning : the exercise corresponding to the attempt is not defined in *exercises*')
        return ''

    # store the attempt's script in a separate file ===============================================
	# str2file(attempt['upload'],'utils/attemptToTest.py')

    # loads the attempt, generates and analyzes the Abstract Syntactic Tree (AST) =================
    nom_module = 'exemple'
    spec = util.spec_from_loader(nom_module, loader=None)
    module_exemple = util.module_from_spec(spec)
    code_exemple = attempt['upload']
    # gestion des input
    if code_exemple.rfind('input()')>0:
        return 'InputError'
    try:
        exec(code_exemple, module_exemple.__dict__)
    except SyntaxError:
        return 'SyntaxError'
    sys.modules['module_exemple'] = module_exemple
    ast = code2astPython(code_exemple)
    # generates the Abstract Running Sequence on testcases ========================================
    aes = ''
	# origin_out = sys.stdout
    for entry in exercise['entries']:
        # generate the trace for the entry ====================================
        if not isinstance(entry,tuple):
            entry = (entry,)
        t = Tracer()
        try:
            trace, resultat, erreur = t.get_trace_and_result(eval('module_exemple.'+exercise['funcname']),*entry)
            aes+=' '+ astTrace2aes(ast, trace, erreur)
        except AttributeError:
            return 'FunctionNameError'
    sys.modules.pop('module_exemple') 
    return aes

if __name__=="__main__":
    from manage import jsonAttempts2data, jsonExercises2data
    NC1014 = jsonAttempts2data('Datasets/NewCaledonia_1014.json')
    NCExercises = jsonExercises2data('Datasets/NewCaledonia_exercises.json')
    for i in range(145):
        print(i)
        c = Code2Aes(NC1014[i],NCExercises)
        #print(c)
