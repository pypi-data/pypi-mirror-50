from mendeleev import element as elem

class glob_element :
	def __init__(self,name,mass,rate,score=1) :
		self.name=name+str(mass)
		self.mass=mass
		self.rate=rate
		self.score=score
		
class material :
	def __init__(self, elements, wt=True) :
		self.elements=[]
		if wt==True :
			total_n=0
			for element in elements :
				total_n+=elements[element]/elem(element).mass
			for element in elements :
				elements[element]=elements[element]/elem(element).mass/total_n
		for system in elements :
			for isotope in elem(system).isotopes :
				if type(isotope.abundance) in (float, int) :
					self.elements.append(glob_element(name=elem(system).symbol,mass=isotope.mass_number,rate=isotope.abundance,score=elements[system]))
				