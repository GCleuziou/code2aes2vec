entrees_visibles = [
         ('c','caledonie'),
 		('e','caledonie'),
 		('u','caledonie'),
 		('z','')
 ]

entrees_invisibles = [
         ('a','ababababab'),
 		('e','ababbbrtfdéèëê'),
 		('r','')
 ]

#@solution
def premiereOccurrenceLettre(lettre,mot):
    pos=None
    for i in range(len(mot)):
 	   if mot[i]==lettre and pos==None:
 		   pos=i
    return pos
