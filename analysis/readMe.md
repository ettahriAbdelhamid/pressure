This note is a copy of the folder analysisPartiallyOld:
This folder is a copy of the analysis folder generated on the 22nd October 2026.
I did this copy so that I can compare plots (and data) before getting more data.
The most important folder here is the pressure folder, the other folders should be the same as in the recent analysis folder.
As far as I know the last update for the pressure Folder was when I did the following
- run 4 different seeds for the lattice 40^3x16 and 4 for 40^3x8 in parallel
- This was done using 8 job arrays, with a time limit of 10 days.   
- Each of this seperate runs should start m=1 and go down to m=0.025. In total for 15 masses (1 0.9 0.8 0.7 0.6 0.5 0.4 0.3 0.2 0.1 0.075 0.05 0.04 0.03 0.025)
- For each mass 200 updates should be done, of which the first 9 updates are accepted even if they should actually be rejected (i planned 10 but i confused < and <=)
- For the masses m=1 down to m=0.3: for the smaller box 200 updates took between 13h 48min and 14h, while for the bigger box they took between 27h 40min and 28h. In this range the time changes only slightly with the mass
- After m=0.3 the bigger boxes could not continue for much longer because the time-limit was reached. For m=0.2 125 updates were completed but since I only save configurations after 50 updates, the newest configuration was for 100 updates.
- The smaller jobs finished the job in time. Now the time for doing the updates depended stronger on the mass. It was 14h 6min for m=0.2 and 15h 20min for m=0.025

Now the somewhat big problem:
=============================
The plan was to start with the first mass using a hot start, which I have done with finer update steps. I think I used (stepSize = 0.02, numStepTraj = 50, numStepStrangeInt = 1, numStepGaugeInt = 10). This should have been done for 50 updates. Then the real simulation should start again with m=1 but the starting config should be the last config of the previous 50 updates. after 200 updates the saved config should then be used as the starting config for the next smaller mass. This should be repeated until the last mass. However my script had a mistake leading to start with a random config for each run (and also random starting random vector but that would be less problematic I think). This happened because I set loadConf=1 instead of 2 (and newRand=0 instead of 1). A second error (which did not matter afterwards anyway) is that it would have loaded the 0th config instead of the 200th of the previous mass because I have confused 2 variables and their role. As I said this wouldn't matter anyway because of the earlier mistake leading to ignore this variable anyway. But even if the earlier error would not have happened the second error would have stopped the script because the 0th config is not saved in the first place.  


This mistake gave me real data, but because the simulations started from a random config, a lot of time was needed to do the thermalization, so for smaller masses I basically have no useful data, because the auto correlation time is too big.


In the recent analysis folder, I did for all simualtions that have already ended with 200 updates 100 more updates.
For the missing masses in the bigger box I run the missing simulations.