from __future__ import print_function
import math
from pso import PSO_new
import logging
from numpy import random, array, linalg, zeros, argmin, argsort
import os
from miniful import *
import copy
from pylab import plot, show

class FuzzyPSO(PSO_new):

	def __init__(self, logfile=None):
		"""
		Creates a new FST-PSO instance.

		Args:
			D: number of dimensions of the problem under optimization
		"""

		super(FuzzyPSO, self).__init__()

		# defaults for membership functions
		self.DER1 = -1.0
		self.DER2 =  1.0
		self.MDP1 = 0.2 
		self.MDP2 = 0.4 
		self.MDP3 = 0.6 
		self.MaxDistance = 0
		self.dimensions = 0
		self._overall_fitness_evaluations = 0
		self._FES = None

		self.enabled_settings = ["cognitive", "social", "inertia", "minvelocity", "maxvelocity", "reboot"]

		self._FITNESS_ARGS = None

		if logfile!=None:
			print (" * Logging to file", logfile, "enabled")
			with open(logfile, 'w'): pass
			logging.basicConfig(filename=logfile, level=logging.DEBUG)
			logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
			logging.info('FST-PSO object created.')

	def enable_decreasing_population(self, FES):
		print (" * Fitness evaluations budget was specified, the 'max_iter' argument will be discarded and the swarm size will be ignored.")
		self.enabled_settings.append("lin_pop_decrease")
		self._FES = FES

	def disable_reboot(self):
		self.enabled_settings = filter(lambda x: x != "reboot", self.enabled_settings)
		print (" * Reboots are DISABLED")

	def disable_fuzzyrule_cognitive(self):
		self.enabled_settings = filter(lambda x: x != "cognitive", self.enabled_settings)
		print (" * Fuzzy rules for cognitive factor DISABLED")

	def disable_fuzzyrule_social(self):
		self.enabled_settings = filter(lambda x: x != "social", self.enabled_settings)
		print (" * Fuzzy rules for social factor DISABLED")

	def disable_fuzzyrule_inertia(self):
		self.enabled_settings = filter(lambda x: x != "inertia", self.enabled_settings)
		print (" * Fuzzy rules for inertia weight DISABLED")

	def disable_fuzzyrule_maxvelocity(self):
		self.enabled_settings = filter(lambda x: x != "maxvelocity", self.enabled_settings)
		print (" * Fuzzy rules for maximum velocity cap DISABLED")

	def disable_fuzzyrule_minvelocity(self):
		self.enabled_settings = filter(lambda x: x != "minvelocity", self.enabled_settings)
		print (" * Fuzzy rules for minimum velocity cap DISABLED")


	def _count_iterations(self, FES):
		NFEcur = 0
		curpop = 0
		SEQ = []
		while (NFEcur<FES):
			curpop = self._get_pop_size(NFEcur)
			NFEcur += curpop
			SEQ.append(curpop)
		#plot(range(len(SEQ)), SEQ);		show()
		return len(SEQ)


	def solve_with_fstpso(self, max_iter=100, creation_method={'name':"uniform"},
		initial_guess_list = None, callback=None, verbose=False, 
		dump_best_fitness=None, dump_best_solution=None):
		"""
			Launches the optimization using FST-PSO. Internally, this method checks
			that we correctly set the pointer to the fitness function and the
			boundaries of the search space.

			Args:
				max_iter: the maximum number of iterations of FST-PSO
				creation_method: specifies the type of particles initialization
				initial_guess_list: the user can specify a list of initial guesses for particles
									to accelerate the convergence (BETA)
				dump_best_fitness: at the end of each iteration fst-pso will save to this file the best fitness value
				dump_best_solution: at the end of each iteration fst-pso will save to this file the structure of the 
				                    best solution found so far
				callback: this argument accepts a dictionary with two items: 'function' and 'interval'. Every 
				          'interval' iterations, the 'function' is called. This functionality can be exploited 
				          to implement special behavior (e.g., restart)
				verbose: enable verbose mode

			Returns:
			    This method returns a couple (optimal solution, fitness of the optimal solution)
		"""
		if self.FITNESS is None:
			print ("ERROR: cannot solve a problem without a fitness function; use set_fitness()")
			exit(-3)

		if self.Boundaries == []:
			print ("ERROR: FST-PSO cannot solve unbounded problems; use set_search_space()")
			exit(-4)

		if self._FES is not None:
			max_iter = self._count_iterations(self._FES)
			print (" * Iterations automatically set to %d" % max_iter)

		self.MaxIterations = max_iter
		self._overall_fitness_evaluations = 0
		self.UseRestart = "reboot" in self.enabled_settings
		if self.UseRestart:
			self._threshold_local_update = max(30, int(max_iter/20))
			print (" * Reboots are activated with theta=%d" % self._threshold_local_update)
			
		print (" * Max iterations set to", self.MaxIterations)
		print (" * Enabled settings:", " ".join(map(lambda x: "[%s]" % x, self.enabled_settings)))

		if "lin_pop_decrease" in self.enabled_settings:
			self.numberofparticles = self._get_pop_size(0)

		print ("\n *** Launching optimization ***")

		print ("* Creating and evaluating particles")

		self.NewCreateParticles(self.numberofparticles, self.dimensions, 
			creation_method=creation_method, initial_guess_list=initial_guess_list)

		self._overall_fitness_evaluations += self.numberofparticles

		result = self.Solve(None, verbose=verbose, callback=callback, dump_best_solution=dump_best_solution, 
			dump_best_fitness=dump_best_fitness)
		
		return result


	def set_search_space(self, limits):
		"""
			Sets the boundaries of the search space.

			Args:
			limits : 2D list or array, shape = (2, dimensions)
					 The dimensions of the problem are automatically determined 
					 according to the length of 'limits'.
		"""
		D = len(limits)
		self.dimensions = D

		self.MaxDistance = max_distance=calculate_max_distance(limits)
		print (" * Max distance: %f" % self.MaxDistance)

		self.Boundaries = limits		
		print (" * Search space boundaries set to:", limits)

		self.MaxVelocity = [  math.fabs(B[1]-B[0]) for B in limits ]
		print (" * Max velocities set to:", self.MaxVelocity)

		self.numberofparticles = int(10 + 2*math.sqrt(D))
		print (" * Number of particles automatically set to", self.numberofparticles)

		logging.info('Search space set (%d dimensions).' % (D))


	def set_swarm_size(self, N):
		"""
			This (optional) method overrides FST-PSO's heuristic and 
			forces the number of particles in the swarm.

		"""
		try:
			N=int(N)
		except:
			print ("ERROR: please specify the swarm size as an integer number")
			exit(-6)

		if N<=1:
			print ("ERROR: FST-PSO cannot work with less than 1 particles, aborting")
			exit(-5)
		else:
			self.numberofparticles = N
			print (" * Swarm size now set to %d particles" % (self.numberofparticles))

		logging.info('Swarm size set to %d particles.' % (self.numberofparticles))


	def call_fitness(self, data, arguments=None):
		if self.FITNESS == None:
			print ("ERROR: fitness function not valid")
			exit(17)
		if arguments==None:	return self.FITNESS(data)
		else:				return self.FITNESS(data, arguments)


	def set_fitness(self, fitness, arguments=None, skip_test=False):		
		"""
			Sets the fitness function used to evaluate the particles.
			This method performs an automatic validation of the fitness function
			(you can disable this feature by setting the optional argument 'skip_test' to True).

			Args:
			fitness : a user-defined function. The function must accept
			a vector of real-values as input (i.e., a candidate solution)
			and must return a real value (i.e., the corresponding fitness value)
			arguments : a dictionary containing the arguments to be passed to the fitness function.
			skip_test : True/False, bypasses the automatic fitness check.
	
		"""	
		if skip_test:
			self.FITNESS = fitness
			self._FITNESS_ARGS = arguments
			self.ParallelFitness = False
			return 

		try:
			print (" * Testing fitness evaluation")
			self.FITNESS = fitness
			self._FITNESS_ARGS = arguments
			self.call_fitness([1e-10]*self.dimensions, self._FITNESS_ARGS)
			self.ParallelFitness = False
			print (" * Test successful")
		except:
			print ("ERROR: the specified function does not seem to implement a correct fitness function")
			exit(-2)


	def set_parallel_fitness(self, fitness, arguments=None, skip_test=False):
		if skip_test:
			self.FITNESS = fitness
			self._FITNESS_ARGS = arguments
			self.ParallelFitness = True
			return 

		np = pso.Particle()
		np.X = [0]*self.dimensions
		self.FITNESS = fitness
		self._FITNESS_ARGS = arguments
		try:
			self.call_fitness([np.X]*self.numberofparticles, arguments)
		except:
			print ("ERROR: the specified function does not seem to implement a correct fitness function")
			exit(-2)
		self.ParallelFitness = True		
		print (" * Test successful")


	def phi(self, f_w, f_o, f_n, phi, phi_max):
		""" 
			Calculates the Fitness Incremental Factor (phi).
		"""

		if phi == 0:
			return 0
		denom = (min(f_w, f_n) - min(f_w, f_o))/f_w			# 0..1
		numer = phi/phi_max									# 0..1		
		return denom*numer


	def CreateFuzzyReasoner(self, max_delta):

		FR = FuzzyReasoner()

		p1 = max_delta*self.MDP1
		p2 = max_delta*self.MDP2
		p3 = max_delta*self.MDP3


		LOW_INERTIA = 0.3
		MEDIUM_INERTIA = 0.5
		HIGH_INERTIA = 1.0

		LOW_SOCIAL = 1.0
		MEDIUM_SOCIAL = 2.0
		HIGH_SOCIAL = 3.0

		LOW_COGNITIVE = 0.1
		MEDIUM_COGNITIVE = 1.5
		HIGH_COGNITIVE = 3.0

		LOW_MINSP = 0
		MEDIUM_MINSP = 0.001
		HIGH_MINSP = 0.01

		LOW_MAXSP = 0.1
		MEDIUM_MAXSP = 0.15
		HIGH_MAXSP = 0.2


		myFS1 = FuzzySet(points=[[0, 0],	[1., 1.], 	[1., 0]], 	term="WORSE")
		myFS2 = FuzzySet(points=[[-1., 0],	[0, 1.],	[1., 0]], 	term="SAME")
		myFS3 = FuzzySet(points=[[-1., 0],	[-1., 1.],	[0, 0]], 	term="BETTER")
		PHI_MF = MembershipFunction( [myFS1, myFS2, myFS3], concept="PHI" )

		myFS4 = FuzzySet(points=[[0, 0],	[0, 1.], 	[p1, 1.], [p2, 0]], 	term="SAME")
		myFS5 = FuzzySet(points=[[p1, 0],	[p2, 1.],	[p3, 0]], 	term="NEAR")
		myFS6 = FuzzySet(points=[[p2, 0],	[p3, 1.],	[max_delta, 1.]], 	term="FAR")
		DELTA_MF = MembershipFunction( [myFS4, myFS5, myFS6], concept="DELTA" )


		myR1 = FuzzyRule( IF(PHI_MF, "WORSE"), 	THEN("INERTIA", LOW_INERTIA), comment="Rule inertia worse phi" )
		myR2 = FuzzyRule( IF(PHI_MF, "WORSE"),	THEN("SOCIAL", HIGH_SOCIAL), comment="Rule social worse phi" )
		myR3 = FuzzyRule( IF(PHI_MF, "WORSE"),	THEN("COGNITIVE", MEDIUM_COGNITIVE), comment="Rule cognitive worse phi" )
		myR4 = FuzzyRule( IF(PHI_MF, "WORSE"), 	THEN("MINSP", HIGH_MINSP), comment="Rule min speed worse phi" )
		myR5 = FuzzyRule( IF(PHI_MF, "WORSE"), 	THEN("MAXSP", HIGH_MAXSP), comment="Rule max speed worse phi" )

		myR6 = FuzzyRule( IF(PHI_MF, "SAME"), 	THEN("INERTIA", MEDIUM_INERTIA), comment="Rule inertia same phi" )
		myR7 = FuzzyRule( IF(PHI_MF, "SAME"),	THEN("SOCIAL", MEDIUM_SOCIAL), comment="Rule social same phi" )
		myR8 = FuzzyRule( IF(PHI_MF, "SAME"),	THEN("COGNITIVE", MEDIUM_COGNITIVE), comment="Rule cognitive same phi" )
		myR9 = FuzzyRule( IF(PHI_MF, "SAME"), 	THEN("MINSP", LOW_MINSP), comment="Rule min speed same phi" )
		myR10 = FuzzyRule( IF(PHI_MF, "SAME"), 	THEN("MAXSP", MEDIUM_MAXSP), comment="Rule max speed same phi" )

		myR11 = FuzzyRule( IF(PHI_MF, "BETTER"), 	THEN("INERTIA", HIGH_INERTIA), comment="Rule inertia better phi" )
		myR12 = FuzzyRule( IF(PHI_MF, "BETTER"),	THEN("SOCIAL", LOW_SOCIAL), comment="Rule social better phi" )
		myR13 = FuzzyRule( IF(PHI_MF, "BETTER"),	THEN("COGNITIVE", HIGH_COGNITIVE), comment="Rule cognitive better phi" )
		myR14 = FuzzyRule( IF(PHI_MF, "BETTER"), 	THEN("MINSP", LOW_MINSP), comment="Rule min speed better phi" )
		myR15 = FuzzyRule( IF(PHI_MF, "BETTER"), 	THEN("MAXSP", MEDIUM_MAXSP), comment="Rule max speed better phi" )


		myR16 = FuzzyRule( IF(DELTA_MF, "SAME"), 	THEN("INERTIA", LOW_INERTIA), comment="Rule inertia same delta" )
		myR17 = FuzzyRule( IF(DELTA_MF, "SAME"),	THEN("SOCIAL", MEDIUM_SOCIAL), comment="Rule social same delta" )
		myR18 = FuzzyRule( IF(DELTA_MF, "SAME"),	THEN("COGNITIVE", MEDIUM_COGNITIVE), comment="Rule cognitive same delta" )
		myR19 = FuzzyRule( IF(DELTA_MF, "SAME"), 	THEN("MINSP", MEDIUM_MINSP), comment="Rule min speed same delta" )
		myR20 = FuzzyRule( IF(DELTA_MF, "SAME"), 	THEN("MAXSP", LOW_MAXSP), comment="Rule max speed same delta" )

		myR21 = FuzzyRule( IF(DELTA_MF, "NEAR"), 	THEN("INERTIA", MEDIUM_INERTIA), comment="Rule inertia near delta" )
		myR22 = FuzzyRule( IF(DELTA_MF, "NEAR"),	THEN("SOCIAL", LOW_SOCIAL), comment="Rule social near delta" )
		myR23 = FuzzyRule( IF(DELTA_MF, "NEAR"),	THEN("COGNITIVE", MEDIUM_COGNITIVE), comment="Rule cognitive near delta" )
		myR24 = FuzzyRule( IF(DELTA_MF, "NEAR"), 	THEN("MINSP", MEDIUM_MINSP), comment="Rule min speed near delta" )
		myR25 = FuzzyRule( IF(DELTA_MF, "NEAR"), 	THEN("MAXSP", MEDIUM_MAXSP), comment="Rule max speed near delta" )

		myR26 = FuzzyRule( IF(DELTA_MF, "FAR"), 	THEN("INERTIA", LOW_INERTIA), comment="Rule inertia far delta" )
		myR27 = FuzzyRule( IF(DELTA_MF, "FAR"),		THEN("SOCIAL", MEDIUM_SOCIAL), comment="Rule social far delta" )
		myR28 = FuzzyRule( IF(DELTA_MF, "FAR"),		THEN("COGNITIVE", MEDIUM_COGNITIVE), comment="Rule cognitive far delta" )
		myR29 = FuzzyRule( IF(DELTA_MF, "FAR"), 	THEN("MINSP", MEDIUM_MINSP), comment="Rule min speed far delta" )
		myR30 = FuzzyRule( IF(DELTA_MF, "FAR"), 	THEN("MAXSP", LOW_MAXSP), comment="Rule max speed far delta" )


		FR.add_rules([myR1, myR2, myR3, myR4, myR5, myR6, myR7, myR8, myR9, myR10,
						myR11, myR12, myR13, myR14, myR15, myR16, myR17, myR18, myR19, myR20,
						myR21, myR22, myR23, myR24, myR25, myR26, myR27, myR28, myR29, myR30 ])

		return FR


	def UpdateCalculatedFitness(self, verbose=False):
		"""
			Calculate the fitness values for each particle according to user's fitness function,
			and then update the settings of each particle.
		"""

		if self.ParallelFitness:
			#print " * Distributing calculations..."
			ripop = map(lambda x: x.X, self.Solutions)
			all_fitness = self.FITNESS(ripop, self._FITNESS_ARGS)
		else:
			all_fitness = []
			for s in self.Solutions:
				# all_fitness.append( self.FITNESS(s.X, self._FITNESS_ARGS ) )
				all_fitness.append( self.call_fitness(s.X, self._FITNESS_ARGS ) )

		fr_cogn = "cognitive" in self.enabled_settings
		fr_soci = "social" in self.enabled_settings
		fr_iner = "inertia" in self.enabled_settings
		fr_maxv = "maxvelocity" in self.enabled_settings
		fr_minv = "minvelocity" in self.enabled_settings


		# for each i-th individual "s"...
		for i,s in enumerate(self.Solutions):

			prev = s.CalculatedFitness
			ret = all_fitness[i]
			if s.MagnitudeMovement != 0:
				s.DerivativeFitness = (ret-prev)/s.MagnitudeMovement

			s.NewDerivativeFitness = self.phi(self.EstimatedWorstFitness, prev, ret, s.MagnitudeMovement, self.MaxDistance)

			if isinstance(ret, list):
				s.CalculatedFitness = ret[0]
				s.Differential = ret[1]
			else:
				s.CalculatedFitness = ret

			####### TEST #######
			
			FR = self.CreateFuzzyReasoner(self.MaxDistance)
			FR.set_variable("PHI", s.NewDerivativeFitness)
			FR.set_variable("DELTA", s.DistanceFromBest)
			res = FR.evaluate_rules()

			
			if fr_cogn: 			s.CognitiveFactor 	= res["COGNITIVE"]
			if fr_soci: 			s.SocialFactor 		= res["SOCIAL"]
			if fr_iner: 			s.Inertia 			= res["INERTIA"]
			if fr_maxv: 			s.MaxSpeedMultiplier = res["MAXSP"]
			if fr_minv: 			s.MinSpeedMultiplier = res["MINSP"]
		
		if "lin_pop_decrease" in self.enabled_settings: 
			indices_sorted_fitness = argsort(all_fitness)[::-1]
			nps = self._get_pop_size(NFEcur = self._overall_fitness_evaluations)
			self._overall_fitness_evaluations += len(self.Solutions)
			if verbose: print (" * Next population size: %d." % nps)

			##### WARNING #####
			self.Solutions = [ self.Solutions[i] for i in indices_sorted_fitness[:nps] ]			
			##### WARNING #####


	def _get_pop_size(self, NFEcur):		
		D = self.dimensions
		heuristic_max = int(math.sqrt(D)*math.log(D))
		heuristic_min = int(10 + 2*math.sqrt(D))
		PSmin = heuristic_min
		PSmax = heuristic_max
		NFEmax = self._FES
		EX = 1
		v = int( (float(PSmin-PSmax)/((NFEmax-PSmax)**EX)) * (NFEcur-PSmax)**EX+PSmax )
		if NFEcur+v>NFEmax:
			return NFEmax-NFEcur
		else:
			return v
		

	def UpdatePositions(self, verbose=False):
		"""
			Update particles' positions and update the internal information.
		"""

		if self.UseRestart:
			if self.Iterations+self._threshold_local_update<self.MaxIterations: 
				for p in self.Solutions:
					if p.MarkedForRestart:
						p.X = self.NewGenerate( zeros(self.dimensions), creation_method = self._used_generation_method )
						p.B = copy.deepcopy(p.X)
						p.V = list(zeros(len(p.X)))
						p.SinceLastLocalUpdate = 0
						p.MarkedForRestart = False
						if verbose: print ("REBOOT happened")

		for p in self.Solutions:	

			prev_pos = p.X[:]

			for n in range(len(p.X)):							
				c1 = p.X[n]
				c2 = p.V[n]
				tv = c1+c2
				rnd1 = rnd2 = 0
				if tv > self.Boundaries[n][1]:
					rnd1 = random.random()
					tv = self.Boundaries[n][1] - rnd1 * c2
				if tv < self.Boundaries[n][0]:
					rnd2 = random.random()
					tv = self.Boundaries[n][0] - rnd2 * c2

				p.X[n] = tv

			p.MagnitudeMovement = linalg.norm(array(p.X)-array(prev_pos), ord=2)
			p.DistanceFromBest = linalg.norm(array(p.X)-array(self.G.X), ord=2)

					

		#logging.info('Particles positions updated.')

	def UpdateVelocities(self):
		"""
			Update the velocity of all particles, according to their own settings.
		"""

		for p in self.Solutions:

			for n in range(len(p.X)):

				fattore1 = p.Inertia * p.V[n]
				fattore2 = random.random() * p.CognitiveFactor * (p.B[n] - p.X[n])
				fattore3 = random.random() * p.SocialFactor * (self.G.X[n] - p.X[n])

				newvelocity = fattore1+fattore2+fattore3

				# check max vel
				if newvelocity > self.MaxVelocity[n] * p.MaxSpeedMultiplier:
					newvelocity = self.MaxVelocity[n] * p.MaxSpeedMultiplier 
				elif newvelocity < -self.MaxVelocity[n] * p.MaxSpeedMultiplier:
					newvelocity = -self.MaxVelocity[n] * p.MaxSpeedMultiplier 

				# check min vel
				if abs(newvelocity) < self.MaxVelocity[n] * p.MinSpeedMultiplier:
					newvelocity = math.copysign(self.MaxVelocity[n] * p.MinSpeedMultiplier, newvelocity)

				# finally set velocity
				p.V[n] = newvelocity

		#logging.info('Particles velocities updated.')


	def TerminationCriterion(self, verbose=False):
		""" 
			This new method for termination criterion verification 
			supports FES exaustion. 
		"""

		if verbose:
			print (" * Iteration:", self.Iterations), 
			print ("   since last global update:", self.SinceLastGlobalUpdate)

		if self.StopOnGoodFitness == True:
			if self.G.CalculatedFitness < self.GoodFitness:
				if verbose:
					print (" * Optimal fitness reached", self.G.CalculatedFitness)
				return True

		if self.SinceLastGlobalUpdate > self.MaxNoUpdateIterations:
			if verbose:
				print ("Too many iterations without new global best")
			return True

		#print (" * Iteration %d: used %d/%d f.e." % (self.Iterations, self._overall_fitness_evaluations, self._FES))

		if self._FES is not None:
			if self._overall_fitness_evaluations>=self._FES:
				print (" * Budget of fitness evaluations exhausted.")
				return True
		else:			
			if self.Iterations > self.MaxIterations:
				if verbose:
					print (" * Maximum iterations reached.")
				return True
			else:
				return False



def calculate_max_distance(interval):
	accum = 0
	for i in interval:
		accum += (i[1]-i[0])**2
	return math.sqrt(accum)


if __name__ == '__main__':
	
	print ("ERROR: please create a new FuzzyPSO object, specify a fitness function and the search space")
