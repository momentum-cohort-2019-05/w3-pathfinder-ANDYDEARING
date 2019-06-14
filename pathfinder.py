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
        self.max_value = self.get_max()
        self.min_value = self.get_min()

    def get_width(self):
        return len(self.data_file)

    def get_length(self):
        return len(self.data_file[0])

    def get_grayscale_value(self, x_coord, y_coord):
        gray_value = int((self.max_value - self.min_value) / 256)
        return int((self.data_file[x_coord][y_coord]-self.min_value) / gray_value)

    def get_min(self):
        list_of_mins = []
        for row in self.data_file:
            list_of_mins.append(min(row))
        # print(min(list_of_mins))
        return min(list_of_mins)

    def get_max(self):
        list_of_maxes = []
        for row in self.data_file:
            list_of_maxes.append(max(row))
        # print(max(list_of_maxes))
        return max(list_of_maxes)

class MapImage:
    def __init__(self, map_data):
        self.map_data = map_data
        self.image = self.build_image()
    
    def show(self):
        self.image.show()

    def build_image(self):
        img = Image.new('RGBA', (map_data.get_width(), map_data.get_length()) )
        return img

# file = input("Which file shall I use? ")
file = "elevation_large.txt"
map_data = MapData(read_file(file))
map_image = MapImage(map_data)
print(map_data.get_grayscale_value(400,400))
# map_image.show()



# print((two_d_elev_list))
# print(len(two_d_elev_list))
# print(len(two_d_elev_list[0]))
