'''
# =============================================================================
#      FileName: base_op.py
#          Desc: 
#        Author: ZaneQi
#         Email: qizheng1993hit@gmail.com
#      HomePage: https://github.com/chouxi
#       Version: 0.0.1
#    LastChange: 2017-03-30 13:23:42
#       History:
# =============================================================================
'''
import time
import numpy as np
from skimage import io, morphology

class base_operation:
    window_size = 5
    margin = 2
    sample = None
    visited_mat = None
    def __init__(self, file_name, window_size):
        self.sample = io.imread(file_name).astype('float64')
        # normalize
        self.sample *= (1.0/self.sample.max())
        # self.window_size need to be odd number
        if self.window_size & 1 == 0:
            self.window_size += 1
        self.margin = self.window_size / 2

    def gaussian2D(self, shape, sigma = 1):
        """
        2D gaussian mask - should give the same result as MATLAB's
        fspecial('gaussian',[shape],[sigma])
        """
        m,n = [(ss-1.)/2. for ss in shape]
        y,x = np.ogrid[-m:m+1,-n:n+1]
        h = np.exp( -(x*x + y*y) / (2.*sigma*sigma) )
        h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
        sumh = h.sum()
        if sumh != 0:
            h /= sumh
        return h

    def get_neighborwind(self, image, pixel):
        x,y = image.shape
        # return indexs instead of the matrix
        return [pixel[0] - self.margin, pixel[0]+1 + self.margin, pixel[1]-self.margin, pixel[1]+1+self.margin]
        
    def find_matches(self, template, image, gauss_mask, sample_block_list, coordinate_list, err_threshold = -1.0):
        valid_mask = self.visited_mat[template[0]:template[1], template[2]: template[3]]
        template_block = image[template[0]:template[1], template[2]: template[3]]
        # get the gauss_mask, shift it make it same to the shape of valid_mask
        if gauss_mask.shape != valid_mask.shape:
            print "[ERROR] gauss_mask shape " + str(gauss_mask.shape) + " is not equal to the valid_mask shape " + str(valid_mask.shape) +""
        weight_mat = np.multiply(gauss_mask, valid_mask)
        total_weight = weight_mat.sum()
        template_block_list = np.tile(template_block, (len(sample_block_list),1,1))
        SSD = np.sum(np.sum(np.multiply(weight_mat, np.square(template_block_list - sample_block_list)), axis=1), axis=1) / total_weight
        threshold = SSD.min()
        if err_threshold != -1.0:
            threshold= threshold*(1+err_threshold)
            pixel_list = []
            for error,coor in zip(SSD, coordinate_list):
                if error <= threshold:
                    pixel_list.append((coor, error))
            return pixel_list
        else:
            for error,coor in zip(SSD, coordinate_list):
                if error == threshold:
                    return (coor, error)
