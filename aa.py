#2sub(image) data structure-----------------------------------------------------------------------------------------------------   
predict = [["image1"],["image2"],["image3"],["image4"],["image5"],["image6"]]


total_list = []   #1)total_list

for image in predict:   
    total_list.append("content")   #2)on each image, append  **one content**  into total_list


print(len(total_list))         #total_list, sub is image 
print(len(total_list[0]))      #image find target(image_list, sub is detection)


  
  
#2sub(image) data structure-----------------------------------------------------------------------------------------------------   
predict = [["image1"],["image2"],["image3"],["image4"],["image5"],["image6"]]


total_list = []   #3)total_list

for image in predict:   
    total_list.append(["content","image.name"])   #4)on each image, append  **one list**  into total_list


print(len(total_list))         #total_list, sub is image                                   #total_list, sub is image 
print(len(total_list[0]))      #image is unknow_list
print(len(total_list[0][0]))   #unknow_list[0] find target(image_list, sub is detection)   #image[0] find target(image_list, sub is detection)    



 