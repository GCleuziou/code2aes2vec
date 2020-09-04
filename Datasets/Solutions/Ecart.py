entrees_visibles = [
        [5,15,10,0],
		[-6,4,-2,0],
		[2],
		[],
]

entrees_invisibles = [
        [5,15,10,0],
		[-6,4,-2,0],
		[2],
		[],
]

#@solution
def ecart(liste):
	if len(liste)==0:
		res=None
	else:
		max=liste[0]
		min=liste[0]
		for i in range(1,len(liste)):
			if liste[i]>max:
				max=liste[i]
			elif liste[i]<min:
				min=liste[i]
		res=max-min
	return res
