from PIL import Image

def read_file(file):
    with open(file) as source_file:
        source_str = source_file.read()
        source_str = source_str.split("\n")
    
    source_two_d_list = []

    for line in source_str:
        if line.split() != []:
            source_two_d_list.append([int(_) for _ in line.split()])

    return source_two_d_list

file = input("Which file shall I use? ")
two_d_elev_list = read_file(file)

print((two_d_elev_list))
print(len(two_d_elev_list))
print(len(two_d_elev_list[0]))

# file  = "elevation_large.txt"
# source_str_2d_list = []
# attempt to store the image in a two dimensional list
# with open(file) as source_file:
#         source_str = source_file.read()

# source_str = source_str.split("\n")

# for line in source_str:
#     if line.split() != []:
#         source_str_2d_list.append([int(_) for _ in line.split()])

# for list_of_str in source_str_2d_list:
#     for elevation in list_of_str:
#         elevation = int(elevation)


    