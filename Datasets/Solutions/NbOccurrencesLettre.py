entrees_visibles = [
        ('e','caledonie'),
		('e','Electricité'),
		('z','')
]

entrees_invisibles = [
        ('a','abcdeaaa'),
		('e','fdereéàzeuèêë'),
		('r','')
]

#@solution
def nbOccurrencesLettre(lettre,mot):
   res=0
   for c in mot:
	   if c==lettre:
		   res+=1
   return res
