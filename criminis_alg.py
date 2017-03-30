'''
# =============================================================================
#      FileName: criminis_alg.py
#          Desc: 
#        Author: ZaneQi
#         Email: qizheng1993hit@gmail.com
#      HomePage: https://github.com/chouxi
#       Version: 0.0.1
#    LastChange: 2017-03-30 10:40:29
#       History:
# =============================================================================
'''
from base_op import *
from skimage import color

class criminis_algorithm:
    base_op = None
    image = None
    def __init__(self, base_op):
        self.base_op = base_op
        self.base_op.sample = color.rgb2gray(self.base_op.sample)

    def remove_blocks(self, block_list):
        self.base_op.visited_mat = np.ones(self.base_op.sample.shape)
        for block in block_list:
            if len(block) < 4:
                print "[ERROR] input block invalid"
            self.base_op.visited_mat[block[0]:block[1], block[2]:block[3]] = 0
        self.base_op.sample = np.multiply(self.base_op.sample, self.base_op.visited_mat)
        io.imshow(self.base_op.sample)
        io.show()
