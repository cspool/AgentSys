# Ramulator2 run 012 analysis

All seven gates pass. Official Ramulator2 exactly accepts the 24,576 LD and 2,176 ST records in both runs and repeats identical stats. One/two-channel memory cycles are 166,400/82,854.

The measured 0.4979 service factor reduces LLaMA2 DE work 1,504→736 but total TISA time only 3,553→3,521 (1.009×), while ME/VE work is unchanged. The result shows that bandwidth scaling has limited benefit after the scheduler shifts the critical path to ME.

