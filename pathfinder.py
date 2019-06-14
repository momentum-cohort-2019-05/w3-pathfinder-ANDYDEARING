from PIL import Image, ImageColor

def read_file(file):
    with open(file) as source_file:
        source_str = source_file.read()
        source_str = source_str.split("\n")
    
    source_two_d_list = []

    for line in source_str:
        # I don't know why I'm getting empty lists, but I can clean them out
        if line.split() != []:
            source_two_d_list.append([int(_) for _ in line.split()])

    return source_two_d_list

class MapData:
    def __init__(self, data_file):
        self.data_file = data_file
        self.max_value = self.get_max()
        self.min_value = self.get_min()

    def get_width(self):
        """return the number of columns"""
        return len(self.data_file[0])

    def get_length(self):
        """return the number of rows"""
        return len(self.data_file)

    def get_grayscale_value(self, row, column):
        gray_value = int((self.max_value - self.min_value) / 256)
        return int((self.data_file[row][column]-self.min_value) / gray_value)

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
        img = Image.new('RGBA', (self.map_data.get_width(), self.map_data.get_length()) )
        for column in range(self.map_data.get_width()):
            for row in range(self.map_data.get_length()):
                # in the data, the format is row, column
                gray_value = self.map_data.get_grayscale_value(row, column)
                # in the image, the format is column, row
                img.putpixel( (column, row), (gray_value,gray_value,gray_value,255) )
        return img
    
    def putpixel(self, column_row_tup, color="green"):
        self.image.putpixel(column_row_tup,ImageColor.getcolor(color, "RGBA"))
        return None

class Pathfinder:
    def __init__(self, map_data, map_image):
        self.map_data = map_data
        self.map_image = map_image
        self.starting_pos = (0,0)
    
    def set_start(self, column, row):
        self.starting_pos = (column, row)
        return None

    def find_greedy_path(self):
        self.map_image.putpixel(self.starting_pos)


file = "elevation_small.txt"
map_data = MapData(read_file(file))
map_image = MapImage(map_data)
pathfinder = Pathfinder(map_data,map_image)
pathfinder.set_start(30,90)
pathfinder.find_greedy_path()
map_image.show()




# file = input("Which file shall I use? ")
# print(map_data.get_grayscale_value(400,400))



# print((two_d_elev_list))
# print(len(two_d_elev_list))
# print(len(two_d_elev_list[0]))
