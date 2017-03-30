'''
# =============================================================================
#      FileName: test.py
#          Desc: 
#        Author: ZaneQi
#         Email: qizheng1993hit@gmail.com
#      HomePage: https://github.com/chouxi
#       Version: 0.0.1
#    LastChange: 2017-03-30 13:48:28
#       History:
# =============================================================================
'''

from base_op import *
from ef_alg import *

if __name__ == '__main__':
    base_op =  base_operation('./pics/T1.gif', 5)
    efros_obj = efros_algorithm(base_op)
    efros_obj.efros_synthesis(50, 50)
    #efros_obj = efros_algorithm('./pics/T1.gif', 5)
    #efros_obj.efros_synthesis(200, 200)
