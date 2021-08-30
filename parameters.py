## erosion

###### original values
weatheringRateBareBedrock=0.0005
#weatheringExponentParameter=4.0    # it seems this should be 4.02359478109, which results in steady state soil depth of 0.4
weatheringExponentParameter=4.02359478109

######## originalWithDecreasedWeathering
#weatheringRateBareBedrock=0.0004
#weatheringExponentParameter=3.4657359

##### originalWithIncreasedWeathering
#weatheringRateBareBedrock=0.002
#weatheringExponentParameter=7.48933068

intercept=10.0

############
# REGO
###########


# this scenario
vegetationRange = 0.28                                      # 0.28, b in paper -> very sensitive should be above 0.22 (fast)
meanErosionRate=0.0008*52.0                                 # 0.0008*52.0 used for paper
factor=2.01                                                 # 2.01 used for paper
erosionRateBareBedrockThickMax = meanErosionRate/factor     # 0.021, E_t in paper -> somewhat sensitive, determ. right side
print('E_t is ', erosionRateBareBedrockThickMax)
erosionRateBareBedrockThickZero = meanErosionRate*factor    # 0.084, E_0 in paper -> somewhat sensitive, determ. left side
print('E_0 is ', erosionRateBareBedrockThickZero)            # ie crosssing with y axis
erosionExponentParameter= 20.0                              # 20, c in paper (later k) (in paper 1/20, 0.05 m) -> somewhat sensitive,
                                                            # determines left side curve


############
# VEG
############

# met zelfde grazing pressure kun je andere shift durations krijgen
# met standaard waarden is sihft op 1.885702, time 5890
# met carryingCap op 3.9 en regolithRange op 0.178 is shift op 1.878 (~ zelfde) en time 17115 (hoger); let op
# dit is bij smallere band above min reg thickness and r at shift, maar VEEL lagere verschilwaarden

# this scenario, note that s in the paper is fixed to 0.4
growthRateParameter=2.1  # 2.1, r in paper -> collapse time is not sensitive
carryingCapacity=2.9     # 2.9, c in paper -> very sensitive 
                         # (can cause slow shift without grazing)
                         # cannot be below minimum reg thickness of regolith function!
                         # (then there is no
                         # stable point anyway)
                         # range 1.5-4.0
                         # scenarios for paper, default weathering (original values),
                         # carrying capacity
                         # 2.3 or 3.5
regolithRange=0.04       # 0.04, d in paper -> very sensitive (can cause fast shift without grazing, at 0.7)
                         # at high values, it seems vegetation system is in equilibrium does not hold
regolithIntercept=-0.7   # -0.7, i in paper -> a bit sensitive
