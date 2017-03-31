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
from skimage import color, filters
import math

class criminis_algorithm:
    base_op = None
    image = None
    origin_sample = None
    isophote_x = None
    isophote_y = None
    boundary_mat = None
    gauss_mask = None
    def __init__(self, base_op):
        self.base_op = base_op
        self.base_op.sample = color.rgb2gray(self.base_op.sample)
        self.origin_sample = self.base_op.sample

    def remove_blocks(self, block_list):
        margin = self.base_op.margin
        sample_x, sample_y = self.base_op.sample.shape
        visited_mat = np.ones(self.base_op.sample.shape)
        for block in block_list:
            if len(block) < 4:
                print "[ERROR] input block invalid"
            visited_mat[block[0]:block[1], block[2]:block[3]] = 0
        self.base_op.sample = np.multiply(self.base_op.sample, visited_mat)
        self.base_op.visited_mat = np.zeros((sample_x + margin * 2, sample_y+ margin*2))
        self.base_op.visited_mat[margin:sample_x + margin, margin: sample_y + margin] = visited_mat
    
    def __init_mats(self):
        enlarge_x, enlarge_y = self.base_op.visited_mat.shape
        margin = self.base_op.margin
        self.isophote_x = filters.scharr_h(self.origin_sample)
        self.isophote_y = filters.scharr_v(self.origin_sample)
        self.image = np.zeros((enlarge_x, enlarge_y))
        self.image[margin: enlarge_x - margin, margin: enlarge_y - margin] = self.base_op.sample
        # specified for boundary and gradient get
        self.boundary_mat = np.ones((enlarge_x, enlarge_y))
        self.boundary_mat[margin: enlarge_x - margin, margin: enlarge_y - margin] = self.base_op.visited_mat[margin: enlarge_x - margin, margin: enlarge_y - margin]
        # get sample block list
        sample_block_list = []
        # get coorsponding coordinate
        coordinate_list = []
        for (x,y),v in np.ndenumerate(self.image):
            if v == 0:
                continue
            tmp = self.base_op.sample[(x - self.base_op.margin):(x+1 + self.base_op.margin),(y-self.base_op.margin):(y+1+self.base_op.margin)]
            if tmp[tmp==0].shape[0] == 0:
                sample_block_list.append(tmp)
                # shift to sample coordinate
                coordinate_list.append((x-self.base_op.margin,y-self.base_op.margin))
            self.base_op.visited_mat[x,y] = 1
        sigma = self.base_op.window_size / 6.4
        self.gauss_mask = self.base_op.gaussian2D((self.base_op.window_size,self.base_op.window_size), sigma)
        return [sample_block_list, coordinate_list]
        
    def __get_priority(self, unfilled_list):
        min_priority = 0.0
        min_pixel = (0,0)
        margin = self.base_op.margin
        gradient_x = filters.scharr_h(self.boundary_mat[margin:self.origin_sample.shape[0] + margin, margin:self.origin_sample.shape[1] + margin])
        gradient_y = filters.scharr_v(self.boundary_mat[margin:self.origin_sample.shape[0] + margin, margin:self.origin_sample.shape[1] + margin])
        for pixel in unfilled_list:
            temp = (pixel[0] - margin, pixel[0] + 1 + margin, pixel[1] - margin, pixel[1] + 1 + margin)
            confidence = self.base_op.visited_mat[temp[0]:temp[1], temp[2]:temp[3]].sum()
            iso_dx = self.isophote_x[pixel[0], pixel[1]]
            iso_dy = self.isophote_y[pixel[0], pixel[1]]
            norm = math.sqrt(iso_dx*iso_dx + iso_dy*iso_dy)
            if norm != 0:
                iso_dx /= norm
                iso_dy /= norm
            dx = gradient_y[pixel[0], pixel[1]]
            dy = -gradient_x[pixel[0], pixel[1]]
            norm = math.sqrt(dx*dx + dy*dy)
            if norm != 0:
                dx /= norm
                dy /= norm
            data = math.fabs(dx*iso_dx + dy*iso_dy)
            priority = data*confidence
            if priority > min_priority:
                min_pixel = pixel
                min_priority = priority
        return min_pixel

    def __get_unfilled_list(self):
        # finding edge
        boundary = filters.laplace(self.boundary_mat)
        # get 2 layers
        # using boundary_mat make innear layer disappear
        return zip(*np.where(np.multiply(boundary, self.boundary_mat) != 0))

    def do_criminis(self):
        sample_block_list, coordinate_list = self.__init_mats()
        margin = self.base_op.margin
        while 1:
            unfilled_list = self.__get_unfilled_list()
            if len(unfilled_list) == 0:
                break
            pixel = self.__get_priority(unfilled_list)
            #print self.image[pixel[0] - self.base_op.margin: pixel[0] + 1 + self.base_op.margin, pixel[1] - self.base_op.margin: pixel[1] + 1 + self.base_op.margin]
            #print self.base_op.visited_mat[pixel[0] - self.base_op.margin: pixel[0] + 1 + self.base_op.margin, pixel[1] - self.base_op.margin: pixel[1] + 1 + self.base_op.margin]
            print ~self.base_op.visited_mat[pixel[0] - self.base_op.margin: pixel[0] + 1 + self.base_op.margin, pixel[1] - self.base_op.margin: pixel[1] + 1 + self.base_op.margin]
            #best_pixel = self.base_op.find_matches([pixel[0]-margin, pixel[0] + 1 + margin, pixel[1] - margin, pixel[1] + 1 + margin], self.image, self.gauss_mask, np.asarray(sample_block_list), coordinate_list)
            break
