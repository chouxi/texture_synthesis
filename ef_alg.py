'''
# =============================================================================
#      FileName: ef_alg.py
#          Desc: 
#        Author: ZaneQi
#         Email: qizheng1993hit@gmail.com
#      HomePage: https://github.com/chouxi
#       Version: 0.0.1
#    LastChange: 2017-03-28 10:56:33
#       History:
# =============================================================================
'''
import matplotlib.pyplot as plt
import random
from base_op import *

class efros_algorithm:
    err_threshold = 0.1
    max_err_threshold = 0.3
    base_op = None
    def __init__(self, base_op):
        self.base_op = base_op
        

    def __get_unfilled_neighbor(self):
        count_mask = np.ones((3,3))
        count_mask[1][1] = 0
        dilation_mat = np.ones((3,3))
        dilation_mask = morphology.dilation(self.base_op.visited_mat, selem=dilation_mat) - self.base_op.visited_mat
        count_dict = {}
        x,y = dilation_mask.shape
        for (i,j),v in np.ndenumerate(dilation_mask):
            if v == 1 and i >= self.base_op.margin and i < x - self.base_op.margin and j >= self.base_op.margin and j < y-self.base_op.margin:
                tmp = self.base_op.visited_mat[i-1:i+2 , j-1:j+2]
                count = int(np.multiply(tmp, count_mask).sum())
                if count_dict.has_key(count):
                    count_dict[count].append((i,j))
                else:
                    count_dict.setdefault(count, [(i,j)])
        count_list = count_dict.keys()
        count_list.sort(reverse=True)
        unfilled_list = []
        for key in count_list:
            unfilled_list += count_dict[key]
        return unfilled_list

    def __grow_image(self, image, sample_block_list, coordinate_list):
        # get gauss2D
        sigma = self.base_op.window_size / 6.4
        gauss_mask = self.base_op.gaussian2D((self.base_op.window_size, self.base_op.window_size), sigma)
        while 1:
            flag = 0
            pixel_list = self.__get_unfilled_neighbor()
            if len(pixel_list) == 0:
                break
            for pixel in pixel_list:
                template = self.base_op.get_neighborwind(image, pixel)
                matches_list = self.base_op.find_matches(template, image, gauss_mask, np.asarray(sample_block_list), coordinate_list, self.err_threshold)
                if matches_list == 1:
                    match_pixel = matches_list[0]
                else:
                    match_pixel = matches_list[random.randrange(len(matches_list))]
                if match_pixel[1] < self.max_err_threshold:
                    image[pixel[0],pixel[1]] = self.base_op.sample[match_pixel[0]]
                    self.base_op.visited_mat[pixel[0],pixel[1]] = 1
                    flag = 1
            if flag == 0:
                self.max_err_threshold *= 1.1
            #io.imshow(image)
            #io.show()

    def efros_synthesis(self, new_x, new_y):
        sample_x, sample_y = self.base_op.sample.shape
        new_x += self.base_op.margin*2
        new_y += self.base_op.margin*2
        #init mats
        image = np.zeros((new_x,new_y))
        self.base_op.visited_mat = np.zeros((new_x,new_y))
        # put sample into the image 
        start_x = new_x / 2 - 1
        start_y = new_y / 2 - 1
        rand_x = random.randrange(sample_x-3)
        rand_y = random.randrange(sample_y-3)
        image[start_x: (start_x + 3), start_y:(start_y + 3)] = self.base_op.sample[rand_x: rand_x+3, rand_y:rand_y + 3]
        self.base_op.visited_mat[start_x: (start_x + 3), start_y:(start_y + 3)] = 1
        # get sample block list
        sample_block_list = []
        # get coorsponding coordinate
        coordinate_list = []
        for x in range(self.base_op.margin, sample_x - self.base_op.margin):
            for y in range(self.base_op.margin, sample_y - self.base_op.margin):
                sample_block_list.append(self.base_op.sample[(x - self.base_op.margin):(x+1 + self.base_op.margin),(y-self.base_op.margin):(y+1+self.base_op.margin)])
                coordinate_list.append((x,y))
        self.__grow_image(image, sample_block_list, coordinate_list)
        image = image[self.base_op.margin: new_x - self.base_op.margin, self.base_op.margin: new_y - self.base_op.margin] *255
        io.imshow(image, cmap='gray')
        io.show()

    def efros_impainting(self):
        sample_x, sample_y = self.base_op.sample.shape
        new_x = sample_x + self.base_op.margin*2
        new_y = sample_y + self.base_op.margin*2
        # init mats
        image = np.zeros((new_x,new_y))
        self.base_op.visited_mat = np.zeros((new_x,new_y))
        # put sample into the image 
        image[self.base_op.margin: new_x - self.base_op.margin, self.base_op.margin:new_y - self.base_op.margin] = self.base_op.sample
        # get sample block list
        sample_block_list = []
        # get coorsponding coordinate
        coordinate_list = []
        for (x,y),v in np.ndenumerate(image):
            if v == 0:
                continue
            tmp = image[(x - self.base_op.margin):(x+1 + self.base_op.margin),(y-self.base_op.margin):(y+1+self.base_op.margin)]
            if tmp[tmp==0].shape[0] == 0:
                sample_block_list.append(tmp)
                coordinate_list.append((x - self.base_op.margin,y - self.base_op.margin))
            self.base_op.visited_mat[x,y] = 1
        self.__grow_image(image, sample_block_list, coordinate_list)
        image = image[self.base_op.margin: new_x - self.base_op.margin, self.base_op.margin: new_y - self.base_op.margin] *255
        io.imshow(image, cmap='gray')
        io.show()
