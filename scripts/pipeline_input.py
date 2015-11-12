import sys
import os
from subprocess import call
#This is the script that is run at the command line for executing the pipeline.
#Add as many read files as needed here. This should automatically run the script for each one.
cmd ="python pipeline.py readset_1.fastq"
call(cmd,shell=True)
cmd ="python pipeline.py readset2_1.fastq"
call(cmd,shell=True)
