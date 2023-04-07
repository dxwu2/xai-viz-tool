# (done) Obtain task network 
# Convert task network into STN where tasks are separated by precedence constraints

import sys
import json

# Returns:
#    content of entire input
#    task network           - list of tasks where each task is a dict
#    precedence constraints - list of lists of precedence constraints (e.g. [[a,b],[c,d]] means a -> b, c -> d)
def read_input():
    f = open(sys.argv[1])
    content = json.load(f)
    f.close()
    return content, content['tasks'], content['precedence_constraints']

def __main__():
    file_contents, task_network, precedence_constraints = read_input()
    

__main__()