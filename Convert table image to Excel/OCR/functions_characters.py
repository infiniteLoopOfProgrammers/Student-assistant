import numpy as np
import cv2
def imw(rect,mo_image,num = 0):
    [x,y,w,h] = rect
    letter = mo_image[y:y+h,x:x+w]
    cv2.imwrite(f'all_letters_in_img3/letter{num}.png', letter)
    
def in_inside(rectGrated,rectSmaler,mo_image) -> bool:
    [x1,y1,w1,h1] = rectGrated
    [x2,y2,w2,h2] = rectSmaler	
    imw(rectGrated,mo_image,1)
    imw(rectSmaler,mo_image,2)
    if(y2>=y1 and  y1+h1>=y2+h2 and x2>=x1 and x2+w2<=x1+w1):
        return True
    return False

def check_inside(rects,j,max_line_height,mo_image) -> bool:
	if((rects[j][3] < max_line_height/2.4)):
		if(in_inside(rects[j-1],rects[j],mo_image)):
			return True
		elif j != len(rects)-1:
			if in_inside(rects[j+1],rects[j],mo_image) :
				return True

def in_up_or_down(rectGrated,rectSmaler,mo_image):
    [x1,y1,w1,h1] = rectGrated
    [x2,y2,w2,h2] = rectSmaler
    imw(rectGrated,mo_image,1)
    imw(rectSmaler,mo_image,2)	
    if(x2>=x1 and x2+w2<=x1+w1):
        return True
    return False

def check_in_up_or_down(rects,j,max_line_height,mo_image) -> int:
	if((rects[j][3] < max_line_height/2.4)): 
		if(in_up_or_down(rects[j-1],rects[j],mo_image)):
			return -1
		elif j != len(rects)-1:
			if in_up_or_down(rects[j+1],rects[j],mo_image) :
				return 1
	return 0

def haveSmallRect(rects,max_line_height) -> bool:
	for courentRect in rects:
		if(courentRect[3] < max_line_height/2.4):
			return True
	return False

 	
def fix_i_j(rect, max_line_height, max_w,mo_image,line,word):
	# ========== correct dots commas
	counter = 0
	while(haveSmallRect(rect,max_line_height) and counter < 50):
		i_dot_list = []
		for j,courentRect in enumerate(rect):
			[x,y,w,h] = courentRect
			imw(rect[j],mo_image)
			if check_inside(rect,j,max_line_height,mo_image):
				i_dot_list.append(j)
				continue
			res  = check_in_up_or_down(rect,j,max_line_height,mo_image)
			if res != 0:
				miny = min(rect[j+res][1],rect[j][1])
				maxEndy = max(rect[j+res][1]+rect[j+res][3],rect[j][1]+rect[j][3])
				rect[j+res] = (rect[j+res][0],miny,rect[j+res][2],maxEndy - miny)
				i_dot_list.append(j)
				imw(rect[j+res],mo_image)
	

	
			# #if the dot of i is the last element in the rect, the [j+1] index will not work. so we put [j-1] separately here
			# if  (j is len(rect)-1 and (h < max_line_height/3)):
			# 	if(abs(rect[j-1][0]+rect[j-1][2] - (x+w)) < max_w/3.5 ):
			# 		imw(rect[j-1],mo_image)
			# 		rect[j-1] = (rect[j-1][0], rect[j-1][1], rect[j-1][2], rect[j-1][3] + (rect[j-1][1] - y))
			# 		rect[j-1] = (rect[j-1][0], y, rect[j-1][2], rect[j-1][3])
			# 		i_dot_list.append(j)
			# 		imw(rect[j-1],mo_image)
			# 	elif (y > (rect[j-1][1] + rect[j-1][3]/3)):
			# 		imw(rect[j],mo_image)
			# 		rect[j] = [x,y-(max_line_height/2),w,h+(max_line_height/2)]
			# 		# imw(rect[j],mo_image)
		
			# #if the dot of i is not the last element in the rect
			# else:
				
			# 	if( (h < max_line_height/3) and (abs(rect[j+1][0]+rect[j+1][2] - (x+w)) < max_w/3.5)):
			# 		imw(rect[j+1],mo_image)
			# 		rect[j+1] = (rect[j+1][0], rect[j+1][1], rect[j+1][2], rect[j+1][3] + (rect[j+1][1] - y))
			# 		rect[j+1] = (rect[j+1][0], y, rect[j+1][2], rect[j+1][3])
			# 		imw(rect[j+1],mo_image)
			# 		i_dot_list.append(j)
					
			# 	elif( (h < max_line_height/3) and (abs(rect[j-1][0]+rect[j-1][2] - (x+w)) < max_w/3.5) ):
			# 		imw(rect[j-1],mo_image)
			# 		rect[j-1] = (rect[j-1][0], rect[j-1][1], rect[j-1][2], rect[j-1][3] + (rect[j-1][1] - y))
			# 		rect[j-1] = (rect[j-1][0], y, rect[j-1][2], rect[j-1][3])
			# 		imw(rect[j-1],mo_image)
			# 		i_dot_list.append(j)

			# 	elif (h < max_line_height/2.4 and y > (rect[j-1][1] + rect[j-1][3]/3)):
			# 		imw(rect[j],mo_image)
			# 		rect[j] = [x,y-(max_line_height/2),w,h+(max_line_height/2)]
			# 		# imw(rect[j],mo_image)
				

		rect = np.delete(rect, i_dot_list, axis=0)
		# =======================
		counter += 1
		
	return rect