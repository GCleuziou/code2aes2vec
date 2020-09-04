entrees_visibles = [
        2021,
		2020,
        2000,
		1900
]
entrees_invisibles = [
        2400,
		2100,
		2111,
		2104
]

#@solution
def bissextile(annee):
   if annee%400==0:
	   res=True
   elif annee%4==0 and annee%100!=0:
	   res=True
   else:
	   res=False
   return res
