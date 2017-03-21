'''
# =============================================================================
#      FileName: ef_alg.py
#          Desc: 
#        Author: ZaneQi
#         Email: qizheng1993hit@gmail.com
#      HomePage: https://github.com/chouxi
#       Version: 0.0.1
#    LastChange: 2017-03-21 18:55:58
#       History:
# =============================================================================
'''
import numpy as np
def get_unfilled_neighbor(visited_mat):
    direction = [(0,1), (0,-1), (-1,0), (1,0)]
    x, y = visited_mat.shape
    unfilled_list = []
    for i in x:
        for j in y:
            if visited_mat[x][y] == 0:
                for k in len(direction):
                    if visited_mat[x+direction[k][0]][y + direction[k][1]] == 1:
                        unfilled_list.append((x, y))
                        break
    return unfilled_list
    
def grow_image(sample, image, visited_mat, window):
    
