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
from criminis_alg import *

if __name__ == '__main__':
    '''
    base_op =  base_operation('./pics/test_im1.bmp', 5)
    efros_obj = efros_algorithm(base_op)
    efros_obj.efros_impainting()
    #efros_obj = efros_algorithm('./pics/T1.gif', 5)
    #efros_obj.efros_synthesis(200, 200)
    '''
    # people
    base_op =  base_operation('./pics/test_im3.jpg', 5)
    criminis_obj = criminis_algorithm(base_op)
    criminis_obj.remove_blocks([(352,485,223,253)])
    criminis_obj.do_criminis()
