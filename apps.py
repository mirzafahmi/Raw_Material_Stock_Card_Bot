import sys
import os
script_dir = os.path.dirname( __file__ )
#access Class file
ProDetect_class_script_dir = os.path.join( script_dir, "Raw_Data" )
sys.path.append(ProDetect_class_script_dir)
from ProDetect_class import ProDetect

PR_DEN_1 = ProDetect("PR_DEN_1", 25)

print(PR_DEN_1.min_potential_produced())

