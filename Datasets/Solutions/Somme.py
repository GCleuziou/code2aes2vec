entrees_visibles = [
        [12,1,25,7],
		[-3,7,18,-12],
        [-12,-1,-25,-7],
		[],
]

entrees_invisibles = [
        [12,1,25,7],
		[-3,7,18,-12],
        [-12,-1,-25,-7],
		[],
]

#@solution
def somme(liste):
   res=0
   for elem in liste:
	   res=res+elem
   return res
