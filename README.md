# minimal_biomass_soil_model
Non-spatial model to simulate semi-arid vegetation-soil systems

This is a lumped (non-spatial) model simulating plant growth coupled to erosion processes
in semi-arid vegetation-soil systems. The equations of the model are described in
Karssenberg, D., Bierkens, M.F.P., Rietkerk, M. (2017), Catastrophic Shifts in Semiarid
Vegetation-Soil Systems May Unfold Rapidly or Slowly, https://doi.org/10.1086/694413.  

The model uses components from the PCRaster Python framework and you need to install
PCRaster to run the model, https://www.pcraster.eu

main.py
Contains the model. It is written in the PCRaster Python framework. See
http://www.pcraster.eu.
The model writes two files with output timeseries for biomass and
regolith thickness. It also writes the grazing pressure.

parameters.py
Contains the parameters. These need to be varied to get different
realizations of the 'reality'. See the article for the explanation
of the parameters. The parameter values in the file correspond to those in the article
and settings for some of the scenarios are provided.

plot.py
Script to plot the timeseries.
Output is timeseries.pdf
