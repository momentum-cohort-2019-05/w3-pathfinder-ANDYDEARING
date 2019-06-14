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

class MapData:
    def __init__(self, data_file):
        self.data_file = data_file
    def get_width(self):
        return len(self.data_file)
    def get_length(self):
        return len(self.data_file[0])

class MapImage:
    def __init__(self, map_data):
        self.map_data = map_data
        self.image = Image.new('RGBA', (map_data.get_width(), map_data.get_length()) )
    
    def show(self):
        self.image.show()

# file = input("Which file shall I use? ")
file = "elevation_small.txt"
map_data = MapData(read_file(file))
map_image = MapImage(map_data)
map_image.show()



# print((two_d_elev_list))
# print(len(two_d_elev_list))
# print(len(two_d_elev_list[0]))
