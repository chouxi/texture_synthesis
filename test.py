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
    base_op =  base_operation('./pics/test_im1.bmp', 11)
    #efros_obj = efros_algorithm(base_op)
    #efros_obj.efros_synthesis(200, 200)
    efros_obj = efros_algorithm(base_op)
    efros_obj.efros_impainting()
    '''
    '''
    base_op =  base_operation('./pics/test_im3.jpg', 9)
    criminis_obj = criminis_algorithm(base_op)
    # people
    #criminis_obj.remove_blocks([(352,485,222,253)])
    # sign
    #criminis_obj.remove_blocks([(513,567,770,830),(566,664,788, 803)])
    # pole
    criminis_obj.remove_blocks([(630, 664,3,390), (600, 630, 3, 435), (570,600,95,490), (540,570, 190,530),(510,540, 283, 570), (480, 510, 390, 610), (465,480, 465, 630),(440,465, 515,660)])
    criminis_obj.do_criminis()
    '''
    base_op =  base_operation('./pics/test_im3.jpg', 9)
    efros_obj = efros_algorithm(base_op)
    # person
    # efros_obj.efros_removal([(352,485,222,253)])
    # pole
    # efros_obj.efros_removal([(630, 664,3,390), (600, 630, 3, 435), (570,600,95,490), (540,570, 190,530),(510,540, 283, 570), (480, 510, 390, 610), (465,480, 465, 630),(440,465, 515,660)])
    # sign
    efros_obj.efros_removal([(513,567,770,830),(566,664,788, 803)])
