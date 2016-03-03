'''
Created on 21/10/2013

@author: Omar
'''
from __future__ import division
import random

class SDE():
    '''
    Clase que define Evolucion diferencial simple       
    '''
    #Limites de Generacion self.population
    lowerbound=None
    upperbound=None
    #Intermediary Population (Mutant and Trial Vectors)
    temp_population=None
    #Actual Working Population Popsize is implicity in len(population)
    population=None
    maxgenerations=None
    maxpop=None
    #Factors of SDE
    factor_mutation=None
    factor_crossover=None
    scale_factor=0
    #Dim of Vector
    vectordim =None
    #Search Limits
    leftlimit =None
    rightlimit =None
    
    def __init__(self,popsize,maxgen,scaleF,factorm,factorc,lowerbound,upperbound,vectordim,leftlimit,rightlimit):
        '''
        Create an instance of SDE with:
        popsize := Maximun size of population
        maxgen := Maximun genetarions allowed (Iterations)
        scalef := Scale factor used in mutation
        factorm , factorc := Mutation factor,Crossover factor
        lowerbound ,upperbound := bounds of starting generation [Min,Max].
        vectordim := Dimension of vector D
        Leftlimit,RightLimit -> Limits for search
        '''
        self.maxpop=popsize
        self.maxgenerations=maxgen
        self.scale_factor=scaleF 
        self.factor_mutation=factorm
        self.factor_crossover=factorc
        self.lowerbound=lowerbound
        self.upperbound=upperbound
        self.vectordim=vectordim
        
        self.population=[]
        self.temp_population=[]
        if(leftlimit<rightlimit):
            self.leftlimit=leftlimit
            self.rightlimit=rightlimit
        else:
            raise RuntimeError('Not Valid Limits')
            
            
        
    def Initialize(self): 
        '''
        Initializes population of generation 0
        with numbers in [lower bound - upper bound]
        in Dimension D
        '''       
        for i in xrange(self.maxpop):
            newvector = []
            for j in xrange(self.vectordim):
                newvector.append(random.uniform(self.lowerbound, self.upperbound))            
            self.population.append(newvector)
    
    def PrintPopulation(self,Evalfunction,isMinimization):
        '''
        Print Current Population.
        '''
        print '\nPopulation Size : %d\n'%(len(self.population))        
        for i in xrange(len(self.population)):
            print '[%d] : %s \tF[i]= %.2f'%(i+1,self.population[i],Evalfunction(self.population[i]))
        if isMinimization==True:            
            print '\nBest Vector %s Fitness %.2f\n'%(self.ChooseMin(Evalfunction))
        else:
            print '\nBest Vector %s Fitness %.2f\n'%(self.ChooseMax(Evalfunction))
    
    def __ChooseVectors(self,current_index):
        '''
        Choose randomly three different vectors and return the selected indexes        
        '''
        r1 = int(random.randrange(self.maxpop)) 
        while(r1 == current_index):
            r1 = int(random.randrange(self.maxpop)) 
        r2 = int(random.randrange(self.maxpop)) 
        while(r2 == current_index or r2 == r1):
            r2 = int(random.randrange(self.maxpop))
        r3 = int(random.randrange(self.maxpop))
        while(r3 == current_index or r3 == r1 or r3 == r2):
            r3 = int(random.randrange(self.maxpop))
        return r1,r2,r3
    
    def Differential_Mutation(self,index,isBestSelected,vSelected):
        '''
        Differential Mutation :
        Recombine vectors to produce POP Ntrail Vectors in
        Temp Population.
        '''
        r1,r2,r3= self.__ChooseVectors(index)
        if isBestSelected==True:
            r1= vSelected
            
        #Select Random Index
        rndindex = random.randint(0, self.vectordim-1)
        #New vector created
        uVector=[0 for i in xrange(self.vectordim)]
        
        for  k in xrange(self.vectordim):
            if random.random() <= self.factor_mutation or k == rndindex:
                uVector[rndindex] = self.population[r3][rndindex] + self.scale_factor*(self.population[r1][rndindex]-self.population[r2][rndindex])
                if (uVector[rndindex] <self.leftlimit or uVector[rndindex] >self.rightlimit):
                    uVector[rndindex] = self.population[i][rndindex]            
            else:
                uVector[rndindex] = self.population[i][rndindex]
                rndindex= (rndindex+1)%self.vectordim
            #Copy all others.
            rndindex = (rndindex+1)%self.vectordim
            
        self.temp_population.append(uVector)
            
    
    def Differential_Exponential_Crossover(self,index):
        '''
        Differential Crossover Exponential :
        Recombine vectors Xi and Vi to produce POP Ntrail Vectors in
        Temp Population Ui.
        '''
        uVector=[0 for i in xrange(self.vectordim)]
        jr=random.randint(0, self.vectordim-1)
        j=jr
        while True:
            uVector[j]=self.temp_population[index][j]
            j= (j+1)%self.vectordim
            if random.random()>=self.factor_crossover and j==jr:
                break
        while (j!=jr):
            uVector[j]=self.population[index][j]
            j= (j+1)%self.vectordim
        self.temp_population[index]=uVector
         
    def Differential_Binomial_Crossover(self,index):
        '''
        Differential Crossover binomial :
        Recombine vectors Xi and Vi to produce POP Ntrail Vectors in
        Temp Population Ui.
        '''
        uVector=[0 for i in xrange(self.vectordim)]
        jr=random.randint(0, self.vectordim-1)
        j=jr
        
        uVector[j]=self.temp_population[index][j]
        j= (j+1)%self.vectordim
        while (j!=jr):
            if random.random()<=self.factor_crossover:
                uVector[j]=self.temp_population[index][j]
            else:
                uVector[j]=self.population[index][j]            
            j= (j+1)%self.vectordim
        
        self.temp_population[index]=uVector
           
    
    def Selection(self,evalfunction,isMinimization):
        '''
        Selection function 
        Evaluates a vector given the evalfunction
        -> evalfunction(vector)
        '''
        if isMinimization==True:            
            for i in xrange(self.maxpop):
                if(evalfunction(self.temp_population[i])<=evalfunction(self.population[i])):
                    self.population[i]=self.temp_population[i]
        else:
            for i in xrange(self.maxpop):
                if(evalfunction(self.temp_population[i])>=evalfunction(self.population[i])):
                    self.population[i]=self.temp_population[i]
            
    def Start(self,evalfunction,crossoverfunction,isMinimization,isBestSelected,lookedvalue):
        '''
        Starts the search of the problem given 
        the crossoverfunction and evalutaion function.
        '''        
        #Initialize Population
        self.Initialize()
        self.PrintPopulation(evalfunction, isMinimization)
        for i in xrange(self.maxgenerations):
            progress=(float(i)/float(self.maxgenerations))*100
            if progress%10==0:
                print '%d%s'%(progress,'%'),                        
            #Clear TemporalPopulation
            self.temp_population = []
            #Choose if is Minimization or Maximization
            if isMinimization==True:                
                x,y=self.ChooseMin(evalfunction)
            else:
                x,y=self.ChooseMax(evalfunction)
            #encontrado en una generacion
            if(y==lookedvalue):                
                break;
            #Mutation
            if isBestSelected ==False:
                for j in xrange(self.maxpop):
                    self.Differential_Mutation(j,isBestSelected,None)
            else:
                best=self.GetBestVectorIndex(evalfunction, isMinimization)
                for j in xrange(self.maxpop):
                    self.Differential_Mutation(j,isBestSelected,best)                
                
            #Crossover
            for j in xrange(self.maxpop):
                crossoverfunction(j)                
                
            self.Selection(evalfunction,isMinimization)
        print '\nGeneracion de Termino: %d\n Mejor Solucion Encontrada: %s Fitness: %.2f'%(i+1,x,y)

    def __GenerateFitnessList(self,evalfunction):
        lista=[]
        for i in xrange(self.maxpop):
            lista.append(evalfunction(self.population[i]))
        return lista
    
    def ChooseMin(self,evalfunction):
        '''
        Returns the best vector and it's fitness from the current population
        '''  
        lista= self.__GenerateFitnessList(evalfunction)
        return self.population[lista.index(min(lista))],min(lista)
    
    def ChooseMax(self,evalfunction):
        '''
        Returns the best vector and it's fitness from the current population
        '''  
        lista= self.__GenerateFitnessList(evalfunction)
        return self.population[lista.index(max(lista))],max(lista)    
    
    def GetBestVector(self,Evalfunction,isMinimization):        
        if isMinimization==True:            
            return self.ChooseMin(Evalfunction)
        else:
            return self.ChooseMax(Evalfunction)
    
    def GetBestVectorIndex(self,Evalfunction,isMinimization):        
        lista= self.__GenerateFitnessList(Evalfunction)
        if isMinimization==True:            
            return lista.index(min(lista))
        else:
            return lista.index(max(lista))
