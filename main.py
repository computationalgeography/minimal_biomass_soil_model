import math
from pcraster import *
from pcraster.framework import *
from functions import *
from parameters import *       # contains the parameter values

# time step is a week
nrOfSamples = 1                # sets the number of monte carlo samples
numberOfTimeSteps=52 * 20000

# this is a class used in PCRaster models
# if you don't want to use PCRaster you can replace it
# by plain Python code that is now in the initial method below
# and a loop over timesteps, in the dynamic
class CatchmentModel(DynamicModel,MonteCarloModel):
  def __init__(self):
    DynamicModel.__init__(self)
    MonteCarloModel.__init__(self)
    setclone('clone.map')
    setrandomseed(101)

  def premcloop(self):
    print('done')

  def initial(self):
    # this is simply some calculations done before the loop (dynamic)
    # timestep duration in hours
    self.timeStepDuration = 7.0 * 24.0

    # normal execution: take all from simpleParameters.py
    # but slope, thickness, and biomass need to be provided
    self.weatheringRateBareBedrock=weatheringRateBareBedrock
    self.weatheringExponentParameter=weatheringExponentParameter

    self.slope=0.0       # grazing pressure, g in paper
    self.thickness=0.3
    self.biomass=2.8

    self.thickLi=[]
    self.bioLi=[]
    self.slopeLi=[]

    self.durationToDegraded=-9999.0
    self.durationToDegradedStored=False

  def dynamic(self):
    # this is simply a loop, you could replace it by a for loop

    # first run it with grazing pressure zero, to reach equilibrium regolith
    # thickness and vegetation biomass. From there on 'start' the run by
    # a linear increase of the grazing pressure, resulting in a shift.
    # Note that it is important the system first reaches equilibrium
    # before starting increasing the grazing pressure (called slope here).
    if self.currentTimeStep() > 10000 * 52:
      self.slope=self.slope+0.00001
    # self.slope = 1.76 # this is the default value in paper for figure 2

    if self.currentTimeStep() % 52 == 0 or (self.currentTimeStep() == 1):
      self.thickLi.append(self.thickness)
      self.bioLi.append(self.biomass)
      self.slopeLi.append(self.slope)

    bioGrowth=growth(self.biomass,self.thickness,carryingCapacity,growthRateParameter, \
              regolithRange, regolithIntercept)
    bioGrazing=grazing(self.biomass, intercept, self.slope)
    self.biomass=self.biomass+self.timeStepDuration*((bioGrowth-bioGrazing)/(365.0*24.0))
    if self.biomass < 0.0:
      self.biomass=0.0
    
    regWeathering=weathering(self.thickness,self.weatheringRateBareBedrock, \
                  self.weatheringExponentParameter)
    regErosion=erosion(self.thickness,self.biomass,erosionRateBareBedrockThickZero, \
               erosionRateBareBedrockThickMax, \
               erosionExponentParameter,vegetationRange)
    self.thickness=self.thickness+(regWeathering-regErosion)/52.0
    if self.thickness < 0.0:
      self.thickness=0.0

    if self.thickness < 0.01 and not self.durationToDegradedStored:
      self.durationToDegraded=self.currentTimeStep()
      self.durationToDegradedStored=True

    if self.currentTimeStep() == numberOfTimeSteps:
      numpy.save('thick.npy',self.thickLi)
      numpy.save('bio.npy',self.bioLi)
      numpy.save('slope.npy',self.slopeLi)
      numpy.save('durationToDegraded.npy',self.durationToDegraded)

  def postmcloop(self):
    print('done')


myModel = CatchmentModel()
dynamicModel = DynamicFramework(myModel, numberOfTimeSteps)
dynamicModel.setQuiet(True)
mcModel = MonteCarloFramework(dynamicModel, nrOfSamples)
mcModel.setForkSamples(True,2)
mcModel.run()
