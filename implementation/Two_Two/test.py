from PIL import Image
import random

## C0 and C1
C0 = [ [[255,255,0,0], [255,255,0,0]], [[0,0,255,255], [0,0,255,255]], [[255,0,255,0], [255,0,255,0]], [[0,255,0,255], [0,255,0,255]] , [[255,0,0,255], [255,0,0,255]], [[0,255,255,0], [0,255,255,0]] ]
C1 = [ [[255,255,0,0], [0,0,255,255]], [[0,0,255,255], [255,255,0,0]], [[255,0,255,0], [0,255,0,255]], [[0,255,0,255], [255,0,255,0]] , [[255,0,0,255], [0,255,255,0]], [[0,255,255,0], [255,0,0,255]] ]


im = Image.open('secret.png') ## Open the original image

im = im.convert("1") ## Convert to black and white (not grayscale)

share1 = Image.new("1", (2*im.size[0], 2*im.size[1]), 0) ## Share1
share2 = Image.new("1", (2*im.size[0], 2*im.size[1]), 0) ## Share2
combined = Image.new("1", (2*im.size[0], 2*im.size[1]), 0)  ## combined share1 and share2

pixels_share1 = share1.load()
pixels_share2 = share2.load()
pixels_combined = combined.load()

pixels = im.load() ## Get the pixel matrix

for i in range(0, im.size[1]): ## traverse the height 
    for j in range(0, im.size[0]): ## traverse the breadth
        ## black pixel
        if (pixels[j, i] == 0):
            ## replace the relevant pixels in Share1 and Share2
            matrix_index = random.randint(0, 5)
            pixels_share1 [j*2, i*2] = C1[matrix_index][0][0]
            pixels_share1 [j*2 + 1, i*2] = C1[matrix_index][0][1]
            pixels_share1 [j*2, i*2 +1] = C1[matrix_index][0][2]
            pixels_share1 [j*2 + 1, i*2 + 1] = C1[matrix_index][0][3]

            pixels_share2 [j*2, i*2] = C1[matrix_index][1][0]
            pixels_share2 [j*2 + 1, i*2] = C1[matrix_index][1][1]
            pixels_share2 [j*2, i*2 +1] = C1[matrix_index][1][2]
            pixels_share2 [j*2 + 1, i*2 + 1] = C1[matrix_index][1][3]
        
        ## white pixel
        if (pixels[j, i] == 255):
            matrix_index = random.randint(0, 5)
            pixels_share1 [j*2, i*2] = C0[matrix_index][0][0]
            pixels_share1 [j*2 + 1, i*2] = C0[matrix_index][0][1]
            pixels_share1 [j*2, i*2 +1] = C0[matrix_index][0][2]
            pixels_share1 [j*2 + 1, i*2 + 1] = C0[matrix_index][0][3]

            pixels_share2 [j*2, i*2] = C0[matrix_index][1][0]
            pixels_share2 [j*2 + 1, i*2] = C0[matrix_index][1][1]
            pixels_share2 [j*2, i*2 +1] = C0[matrix_index][1][2]
            pixels_share2 [j*2 + 1, i*2 + 1] = C0[matrix_index][1][3]

## 'or' The two shares to check the correctness
for i in range(0, 2*im.size[1], 1):
    for j in range(0, 2*im.size[0], 1):
        if (pixels_share1 [j, i] == 255 and pixels_share2 [j,i] == 255):
            pixels_combined[j,i] = 255
        else:
            pixels_combined[j,i] = 0


share1.save("share1.png")
share2.save("share2.png")
combined.save("combined.png")
combined.show()
im.save("newImage.png")