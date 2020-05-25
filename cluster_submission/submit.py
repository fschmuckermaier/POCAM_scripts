import os
import sys
import time
from os.path import join, exists

# executable
executable = '/path/executable.sh'
mem        = 10 #GB

#data dir name
project_name='test'

#output folder
out_folder='/data/user/fschmuckermaier/data_raw/' + project_name
if not exists(out_folder):
    print('Create a Directory in {}'.format(out_folder))
    os.makedirs(out_folder)


log_str='/scratch/fschmuckermaier/' + project_name #path for log file

args        = out_folder
submit_info = 'executable  = {script} \n\
               universe    = vanilla \n\
               initialdir = /home/fschmuckermaier \n\
               request_gpus = 1 \n\
               request_memory = {mem}GB \n\
               log         = {log}.log \n\
               output      = {out}.out \n\
               error       = {out}.err \n\
               arguments   = "{args}" \n\
               transfer_executable = True \n\
               queue 1 \n'.format(script = executable,
                                  mem    = mem,
                                  out    = out_folder,
                                  args   = args,
			              	      log    = log_str
                                 )

# write submit file
sub_file = 'submit.sub'
with open(sub_file, 'w') as f:
    f.write(submit_info)

# submit them
os.system("condor_submit {}".format(sub_file))

