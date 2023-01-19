import copy
import math
from PIL import Image
import random

## Returns tuple of factors with minimum difference 
def factor(x):
    squareRoot = math.floor(math.sqrt(x))
    squareRoot = int(squareRoot)
    for i in range (0, squareRoot, 1):
        if ( (x % ((squareRoot) - i)) == 0):
            return ((squareRoot - i), x//(squareRoot - i))


##  Function to compute power set
##  1st argument: The set whose power set is to be calculated
##  2nd argument: index of set till which you want to calculate the powersets
##  3rd argument: the current calculated power set
def powerset(set, current_index, current_powerset):
    if (current_index == -1):
        phi = []
        current_powerset.append(phi)
        return
    else:
        powerset(set, current_index -1, current_powerset)
        temp_li = copy.deepcopy(current_powerset)
        for i in range (0, len(current_powerset), 1):
            temp_li[i].append(set[current_index ])
            current_powerset.append(temp_li[i])
        return


## take the input
k = int (input("Enter k: "))
## First generate one each of S0 and S1 matrices 
## And then randomly choose the columns for giving out white and black shares

## find the best dimension of the replacement pixel-sets

dimension = factor(2**(k-1))

set = list(range(k))
current_index = k-1
power_set = []
powerset(set, current_index, power_set)
## power set now has all the subsets
## now seperate out the even and the odd sets
even_sets = []
odd_sets = []
for i in range (0, len(power_set), 1):
    if ( len(power_set[i]) % 2 == 0):
        even_sets.append(power_set[i])
    else:
        odd_sets.append(power_set[i])
## even_sets has all the even cardinality sets
## odd_sets has all the odd cardinality sets

S0 = []
S1 = []
for j in range(0, len(even_sets), 1):
    column_j0 = [0] * len(set)
    column_j1 = [0] * len(set)
    for i in range(0, len(set), 1):
        if (set[i] in even_sets[j]):
            column_j0 [i] = 1
        if (set[i] in odd_sets[j]):
            column_j1 [i] = 1
        
    ## now column_j0 and column_j1 are built
    S0.append(column_j0)
    S1.append(column_j1)
## now S0 and S1 are built

im = Image.open("secret.png")
im = im.convert("1") ## Convert to black and white (not grayscale)
im_pixels = im.load()


share_li = []
for i in range (0, k, 1):
    share_li.append( Image.new("1", (dimension[0]*im.size[0], dimension[1]*im.size[1]), 0) )

share_pixels_li = []
for i in range (0, k, 1):
    share_pixels_li.append( share_li[i].load() )

combined = Image.new("1", (dimension[0]*im.size[0], dimension[1]*im.size[1]), 0)  ## combined share1 and share2 . . .
combined_pixels = combined.load()

for i in range (0, im.size[1] , 1):   ## traverse the height 
    for j in range (0, im.size[0], 1):   ## traverse the breadth
        ## Black pixel
        if (im_pixels [j, i] == 0):
            ## Select a random matrix from C1

            ## Now traverse the share_pixel list
            random.shuffle(S1) 
            for share in range(0, len(share_pixels_li), 1):
                for index in range (0, len(S1), 1):      ###### Replace len(C1[0]) with len(S1)
                    if (S1[index][share] == 0): ##### Here instead of C[matrix_index] use that random matrix
                        share_pixels_li[share][j*dimension[0]+(index%dimension[0]), i*dimension[1]+(index//dimension[1])] = 255
                    else:
                        share_pixels_li[share][j*dimension[0]+(index%dimension[0]), i*dimension[1]+(index//dimension[1])] = 0
        ## White pixel
        if (im_pixels[j, i] == 255):
            ## Select a random matrix from C0

            random.shuffle(S0)
            ## Now traverse the share_pixel list 
            for share in range(0, len(share_pixels_li), 1):
                for index in range (0, len(S0), 1):
                    if (S0[index][share] == 0):
                        share_pixels_li[share][j*dimension[0] +(index%dimension[0]), i*dimension[1]+(index//dimension[1])] = 255
                    else:
                        share_pixels_li[share][j*dimension[0]+(index%dimension[0]), i*dimension[1]+(index//dimension[1])] = 0
                  

for i in range(0, len(share_li), 1):
    s = "share" + str(i+1) + ".png"
    share_li[i].save(s)


for i in range(0, dimension[1]*im.size[1], 1):
    for j in range (0, dimension[0]*im.size[0], 1):
        black_found = False
        for x in range (0, len(share_pixels_li), 1):
            if ( share_pixels_li[x] [j, i] == 0):
                black_found = True
                break
        if (black_found):
            combined_pixels[j, i] = 0
        else:
            combined_pixels[j, i] = 255


combined.save("combined.png")
combined.show()