entrees_visibles = [
        (11.0,12.0),
		(12.0,9.0),
		(9.0,12.0),
		(8.0,9.0)
]
entrees_invisibles = [
        (9.9,19.0),
		(19.0,9.0),
		(10.0,10.0),
		(7.0,9.0),
		(12.0,15.0)
]

#@solution
def semestreValide(ue1,ue2):
	if ue1>=10 :
		if ue2>=10:
			res=True
		elif (ue1+ue2)/2>=10:
			res=True
		else:
			res=False
	else:
		res=False
	return res
