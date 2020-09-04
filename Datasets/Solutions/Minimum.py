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
def minimum(liste):
   if len(liste)==0:
      return None
   res=liste[0]
   for i in range(1,len(liste)):
      if liste[i]<res:
         res=liste[i]
   return res
