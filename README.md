# texture_synthesis
  This is Assignment2 of CS534 computer vision in Rutgers.

- Part1

  texture synthesis using efros Alg

- Part2

  picture impainting using efros Alg

- Part3

  picture impainting after object removal based on criminis's approach.
  
There are 3 classes,
- base_op
  
  Basic operations of images, such as open images, normalization, init mask, init windowsize.
- efors_algorithm

  Combination of part1 and part2 algorithm.
- criminis_algorithm

  The implementation of part3

## How to run
  The main test file is test.py.

  If you want to run, you need to uncomment the comment part in the test.py.
  
  The basic idea to run code is first create an object of base_operation with file_name and the window size. Then create different objects for different part, then call the corresponding functions.

- Part 1:
	```python
    base_op =  base_operation('./pics/tT1.gif', 11)
    efros_obj = efros_algorithm(base_op)
    efros_obj.efros_synthesis(200, 200)
	```
	Only change the './pics/tT1.gif' to different files and 11 to different window size.

- Part 2:
	```python
    base_op =  base_operation('./pics/test_im1.bmp', 11)
    efros_obj = efros_algorithm(base_op)
    efros_obj.efros_impainting()
	```

	Only change the './pics/test_im1.bmp' to different files and 11 to different window size.

- Part 3:

	Criminis
	```python
    base_op =  base_operation('./pics/test_im3.jpg', 9)
    # crinimis part
    criminis_obj = criminis_algorithm(base_op)
    # people
    criminis_obj.remove_blocks([(352,485,222,253)])
    criminis_obj.do_criminis()
	```
	Change list in the remove_blocks for different part to remove. Already listed the listes with comment in the code.

	Efros
	```python
    base_op =  base_operation('./pics/test_im3.jpg', 9)
    efros_obj = efros_algorithm(base_op)
    #person
    efros_obj.efros_removal([(352,485,222,253)])
	```
	similar to criminis.

Very easy to run the code based on the OO.

- Part 4:
	
	run PatchBasedSynthesis.py.
	
	Because cv2 cannot open gif files, I resaved the gifs to jpgs.

	`PatchBasedSynthesis.py /image/source.jpg Patch_Size Overlap_Width Initial_Threshold_error`

	For example,
	
	`python PatchBasedSynthesis.py ./pics/T1.jpg 24 4 5.0`
