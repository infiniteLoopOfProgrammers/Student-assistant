import cv2
from segmentation_word_code.segmentation_words import get_words
from segmentation_characters import get_characters
from user_input import get_string_from_nn
from dict import correction

img_url = "testImg/a1.png"
raw_image = cv2.imread(img_url,0)
cv2.imwrite('./out/o1.png', raw_image)
all_words, words_on_line, max_height_on_line = get_words(raw_image)

print ("no. of lines = ",len(words_on_line))
print (words_on_line)
print ("no. of words = ",len(all_words))


# fp = open("output.txt", 'w')
# fp.truncate()
# use_dict = True
count = 0
for i in range(0, len(words_on_line)):
    for j in range(0, words_on_line[i]):
        all_characters = get_characters(all_words[count],max_height_on_line[i],i,j)
        
#         if use_dict:
#             print( correction(get_string_from_nn(all_characters)))
#             fp.write(correction(get_string_from_nn(all_characters)))
#             fp.write(" ")
#         else:
            # print( get_string_from_nn(all_characters))
            # fp.write(get_string_from_nn(all_characters))
            # fp.write(" ")
            
#         # exit(0)
#         # cv2.imshow("all_words[count]",all_words[count])
#         # cv2.waitKey()
        
        count = count + 1
        
#     print( "\n")
#     fp.write("\n")

# fp.close()