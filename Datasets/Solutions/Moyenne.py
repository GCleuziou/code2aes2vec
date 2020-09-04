entrees_visibles = [
        [5,15],
		[-6,-4,-2,0],
		[],
]

entrees_invisibles = [
        [12,1,25,7],
		[-3,7,18,-12],
        [-12,-1,-25,-7],
]

#@solution
def moyenne(liste):
	if len(liste)==0:
		res=None
	else:
		res=0
		for elem in liste:
			res+=elem
		res=res/len(liste)
	return res
