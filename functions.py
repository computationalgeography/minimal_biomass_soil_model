import numpy
import os

##################
# regolith model #
##################

# main functions

def multiplierErosion(biomass,range):
  return numpy.exp(-biomass/range) 

def weathering(thickness,weatheringRateBareBedrock,weatheringExponentParameter):
  creep=0.0001 # C in the paper
  weathering=weatheringRateBareBedrock * numpy.exp(-weatheringExponentParameter * thickness)-creep
  return weathering

def getWeatheringExponentParameter(creep,weatheringRateBareBedrock,thicknessEqui):
  # returns the weathering exponent for a particular value of the weathering rate
  weatheringExponentParameter=0.0-numpy.log(creep/weatheringRateBareBedrock)/thicknessEqui
  return weatheringExponentParameter

def erosion(thickness,biomass,erosionRateBareBedrockThickZero,erosionRateBareBedrockThickMax, \
            erosionExponentParameter,vegetationRange):
  #dr/dt=  w * numpy.exp(-e * r)-c  -  exp(-biomass/v)*(m + exp(-p * r)*(z-m) )
  #w=weatheringRateBareBedrock, W0 in paper
  #e=weatheringExponentParameter, a in paper
  #r=thickness, D in paper
  #c=creep, C in paper
  #p=erosionExponentParameter, 1/c in paper!!
  #z=erosionRateBareBedrockThickZero, E0 in paper
  #m=erosionRateBareBedrockThickMax, Et in paper
  #v=vegetationRange, b in paper
  erosionBare=numpy.exp(-erosionExponentParameter * thickness)*(erosionRateBareBedrockThickZero- \
              erosionRateBareBedrockThickMax) + erosionRateBareBedrockThickMax
  erosion=erosionBare * multiplierErosion(biomass,vegetationRange)
  return erosion
  
# one dimensional analysis

def biomassOneD(thickness,weatheringRateBareBedrock,weatheringExponentParameter,erosionExponentParameter, \
            erosionRateBareBedrockThickZero, erosionRateBareBedrockThickMax,vegetationRange):
  # written using symbols as in paper
  # biomass = - b * (numpy.log(( W0 * numpy.exp(-a * D)-C ) /  (numpy.exp(-(1/c) * D)*(E0-Et) + Et))) 
  #
  w=weatheringRateBareBedrock
  e=weatheringExponentParameter
  r=thickness
  creep=0.0001
  c=creep
  p=erosionExponentParameter 
  z=erosionRateBareBedrockThickZero
  m=erosionRateBareBedrockThickMax
  v=vegetationRange
  #weathering=w * numpy.exp(-e * r)-c
  #erosion=(exp(-p * r)*(z-m) + m) * exp(-biomass/v) 
  #dr/dt= ( w * numpy.exp(-e * r)-c ) - ( (exp(-p * r)*(z-m) + m) * exp(-biomass/v) )
  #0 = ( w * numpy.exp(-e * r)-c ) - ( (exp(-p * r)*(z-m) + m) * exp(-biomass/v) )
  #- ( w * numpy.exp(-e * r)-c ) =  - (exp(-p * r)*(z-m) + m) * exp(-biomass/v) 
  #( w * numpy.exp(-e * r)-c ) /  (exp(-p * r)*(z-m) + m) = exp(-biomass/v) 
  #ln(( w * numpy.exp(-e * r)-c ) /  (exp(-p * r)*(z-m) + m)) = -biomass/v 
  #- v * (ln(( w * numpy.exp(-e * r)-c ) /  (exp(-p * r)*(z-m) + m))) = biomass
  #print (( w * numpy.exp(-e * r)-c ) /  (numpy.exp(-p * r)*(z-m) + m))
  biomass = - v * (numpy.log(( w * numpy.exp(-e * r)-c ) /  (numpy.exp(-p * r)*(z-m) + m))) 
  return biomass


####################
# biomass model    #
####################

# main functions

def multiplierGrowth(regolith,range, intercept):
  return (1.0-numpy.exp(-regolith/range))*(1.0 - intercept) + intercept

def growth(biomass,thickness,carryingCapacity,growthRateParameter, regolithRange, regolithIntercept):
  growthRateThickReg=growthRateParameter * biomass * ( 1.0 - (biomass/carryingCapacity))
  multi=multiplierGrowth(thickness,regolithRange, regolithIntercept)
  growthRate=growthRateThickReg * multi
  return growthRate

#def grazing(biomass, intercept, slope):
#  grazing=intercept+slope * biomass
#  return grazing

def grazing(biomass, intercept, slope):
  # this one is with 0.01 grazing intercept
  #grazing=0.01+slope*(biomass/(0.4+biomass))
  # this one is with 0.01 grazing intercept removed!
  grazing=slope*(biomass/(0.4+biomass))
  return grazing

# growth minus grazing is (seperately called in mainSimple.py)
#db/dt= ((1.0-numpy.exp(-r/a))*(1.0 - i) + i)  * (g * b * ( 1.0 - (b/c))) - (0.01+s*(b/(0.4+b)))
#  i=regolithIntercept, < 0 , i in paper
#  s=slope, g in paper
#  b=biomass
#  g=growthRateParameter, r in paper
#  c=carryingCapacity, c in paper
#  a=regolithRange, d in paper


# one dimensional analysis

def regThick(biomass,carryingCapacity,growthRateParameter, regolithRange, regolithIntercept, slope):
  # with symbols like in the paper
  # r = - numpy.log(1.0 - ( -i + (0.01+g*(biomass/(0.4+biomass))) / (r * biomass * ( 1.0 - (biomass/c))) ) / (1.0-i)) * d
  #
  #r= (g * b * ( 1.0 - (b/c))) * ((1.0-numpy.exp(-r/a))*(1.0 - i) + i) - (0.01+s*(b/(0.4+b)))
  #
  #db/dt= (g * b * ( 1.0 - (b/c))) * ((1.0-numpy.exp(-r/a))*(1.0 - i) + i) - (0.01+s*(b/(0.4+b)))
  #(0.01+s*(b/(0.4+b))) = (g * b * ( 1.0 - (b/c))) * ((1.0-numpy.exp(-r/a))*(1.0 - i) + i) 
  #-i + (0.01+s*(b/(0.4+b))) / (g * b * ( 1.0 - (b/c))) = (1.0-numpy.exp(-r/a))*(1.0 - i)
  #( -i + (0.01+s*(b/(0.4+b))) / (g * b * ( 1.0 - (b/c))) ) / (1.0-i) = 1.0-exp(-r/a)
  #1.0 - ( -i + (0.01+s*(b/(0.4+b))) / (g * b * ( 1.0 - (b/c))) ) / (1.0-i) = exp(-r/a)
  #-r/a = ln(1.0 - ( -i + (0.01+s*(b/(0.4+b))) / (g * b * ( 1.0 - (b/c))) ) / (1.0-i))
  #r = - ln(1.0 - ( -i + (0.01+s*(b/(0.4+b))) / (g * b * ( 1.0 - (b/c))) ) / (1.0-i)) * a
  i=regolithIntercept
  s=slope
  b=biomass
  g=growthRateParameter
  c=carryingCapacity
  a=regolithRange
  # this one is with 0.01 grazing intercept
  #r = - numpy.log(1.0 - ( -i + (0.01+s*(b/(0.4+b))) / (g * b * ( 1.0 - (b/c))) ) / (1.0-i)) * a
  # this one is with 0.01 grazing intercept removed!
  r = - numpy.log(1.0 - ( -i + (0.0+s*(b/(0.4+b))) / (g * b * ( 1.0 - (b/c))) ) / (1.0-i)) * a
  return r

###############
# analysis functions one dimensional analysis
###############

def parametersOfALine(x1,y1,x2,y2):
  # y = ax + b
  a=(y2-y1)/(x2-x1)
  b=y1-a*x1
  return a,b 

def crossLoc(a,b,A,B):
  x=(b-B)/(A-a)
  y=a*x+b
  return x,y

def vectorsCross(x1,y1,x2,y2,X1,Y1,X2,Y2):
  a,b=parametersOfALine(x1,y1,x2,y2)
  A,B=parametersOfALine(X1,Y1,X2,Y2)
  x,y=crossLoc(a,b,A,B)
  crossx= ((x > x1) and (x < x2)) or ((x < x1) and (x > x2))
  crossX= ((x > X1) and (x < X2)) or ((x < X1) and (x > X2))
  cross=crossx and crossX
  return cross


def findEq(carryingCapacity,growthRateParameter, regolithRange, regolithIntercept, slope, \
  weatheringRateBareBedrock,weatheringExponentParameter,erosionExponentParameter, \
  erosionRateBareBedrockThickZero, erosionRateBareBedrockThickMax,vegetationRange):
  equilibriumFound=False
  #biomass=numpy.arange(0.5,2.8,0.001)
  #biomass=numpy.arange(0.5,50.0,0.01)
  biomass=numpy.arange(0.5,3.0,0.0001)
  thickness=regThick(biomass,carryingCapacity,growthRateParameter, regolithRange, regolithIntercept, slope)
  firstLines=[]
  for i in range(1,len(biomass)-1):
    x1=thickness[i]
    y1=biomass[i]
    x2=thickness[i+1]
    y2=biomass[i+1]
    firstLines.append([x1,y1,x2,y2])
   
  #thick=numpy.arange(0.1,0.4,0.001)
  #thick=numpy.arange(0.01,0.8,0.01)
  thick=numpy.arange(0.05,0.4,0.001)
  bio=biomassOneD(thick,weatheringRateBareBedrock,weatheringExponentParameter,erosionExponentParameter, \
           erosionRateBareBedrockThickZero, erosionRateBareBedrockThickMax,vegetationRange)
  secondLines=[]
  for i in range(1,len(thick)-2):
    x1=thick[i]
    y1=bio[i]
    x2=thick[i+1]
    y2=bio[i+1]
    secondLines.append([x1,y1,x2,y2])

  for firstLine in firstLines:
    for secondLine in secondLines:
      #print firstLine, secondLine
      cross=vectorsCross(firstLine[0],firstLine[1],firstLine[2],firstLine[3], \
                         secondLine[0],secondLine[1],secondLine[2],secondLine[3])
      if cross:
        print('found')
        equilibriumFound=True
        # the last crossing turns out to be the stable one so this is printed
        first=firstLine
        second=secondLine
  if equilibriumFound:
    X=(first[0]+first[2])/2.0
    Y=(first[1]+first[3])/2.0
    x=(second[0]+second[2])/2.0
    y=(second[1]+second[3])/2.0
    return (X+x)/2.0, (Y+y)/2.0
  else:
    return 0.0,0.0
      

#def findEquilibria(carryingCapacity,growthRateParameter, regolithRange, regolithIntercept, slopes, \
#  weatheringRateBareBedrock,weatheringExponentParameter,erosionExponentParameter, \
#  erosionRateBareBedrockThickZero, erosionRateBareBedrockThickMax,vegetationRange):
#  for slope in slopes:
#    x,y=findEq(carryingCapacity,growthRateParameter, regolithRange, regolithIntercept, slope, \
#    weatheringRateBareBedrock,weatheringExponentParameter,erosionExponentParameter, \
#    erosionRateBareBedrockThickZero, erosionRateBareBedrockThickMax,vegetationRange)
#    print slope,x,y

# in main.py these are the command line arguments:
# 1: find equilibrium (1 or 0)
# 2: pass weathering parameters (1 or 0)
# 3: slope
# 4: thickness
# 5: biomass
# 6: weatheringRateBareBedrock
# 7: weatheringExponentParameter
    
def findEquilibriaWithDiffEq(slopes):
  slopesOut=[]
  thicknesses=[]
  biomasses=[]
  for slope in slopes:
    command = 'python mainSimple.py ' + str(slope)
    print(command)
    os.system('python mainSimple.py ' + str(slope))
    equi=numpy.load('equi.npy')
    print(equi)
    slopesOut.append(slope)
    thicknesses.append(equi[0])
    biomasses.append(equi[1])
  numpy.save('slopesEqui.npy',slopesOut)
  numpy.save('thicknessesEqui.npy',thicknesses)
  numpy.save('biomassesEqui.npy',biomasses)
  return slopesOut, thicknesses, biomasses

def findShift(startSlope,passWeatheringParameters, weatheringRateBareBedrock, \
              weatheringExponentParameter):
  slope=startSlope
  biomass = 0.0
  while biomass < 0.1:
    #slope=slope-0.01
    #slope=slope-0.001
    slope=slope-0.0005
    if passWeatheringParameters:
      command = 'python mainSimple.py 1 1 ' + str(slope) + ' -9999 -9999 ' + \
                ' ' + str(weatheringRateBareBedrock) + ' ' + \
                str(weatheringExponentParameter)
    else:
      command = 'python mainSimple.py 1 0 ' + str(slope)
    print(command)
    os.system(command)
    equi=numpy.load('equi.npy')
    thickness=equi[0]
    biomass=equi[1]
    print(slope, thickness, biomass)
  numpy.save('slopeEqui.npy',slope)
  numpy.save('thicknessEqui.npy',thickness)
  numpy.save('biomassEqui.npy',biomass)
  return slope, thickness, biomass
