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

    def get_value(self, column, row):
        try:
            return self.data_file[row][column]
        except:
            return None

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
    
    def putpixel(self, column_row_tup, color="red"):
        # print(column_row_tup)
        self.image.putpixel(column_row_tup,ImageColor.getcolor(color, "RGBA"))
        return None
    
    def save(self, path):
        self.image.save(path)
        return None

class Pathfinder:
    def __init__(self, map_data, map_image):
        self.map_data = map_data
        self.map_image = map_image
        self.curr_pos = (0,0)
        self.total_delta = 0
    
    def set_start(self, column, row):
        self.curr_pos = (column, row)
        self.total_delta = 0
        return None

    def get_column(self):
        return self.curr_pos[0]

    def get_row(self):
        return self.curr_pos[1]

    def find_greedy_path(self, color="red"):
        # draw the starting point
        self.map_image.putpixel(self.curr_pos)
        # move from left to right via the greedy algorithm
        for _ in range(self.map_data.get_width()-self.curr_column()-1):
            curr_row = self.get_row()
            curr_column = self.get_column()
            right_move_tup = self.get_greedy_move( (curr_column+1,curr_row+1), (curr_column+1, curr_row), (curr_column+1, curr_row-1) )
            self.curr_pos = right_move_tup
            # print("right_move_tup", right_move_tup)
            self.map_image.putpixel(self.curr_pos, color)

    def get_greedy_move(self, up_right, right, down_right):
        """recieves three tuples of (column, row) data (potentially None) and
        selects the best move by the greedy algorithm, returning a (column,row)
        tuple"""
        curr_elevation = self.map_data.get_value(self.get_column(),self.get_row())
        new_moves = {}
        # breakpoint()
        new_elevation = map_data.get_value(up_right[1],up_right[0])
        if new_elevation is not None:
            new_moves[up_right] = abs(curr_elevation-new_elevation)
        new_elevation = map_data.get_value(right[1],right[0])
        if new_elevation is not None:
            new_moves[right] = abs(curr_elevation-new_elevation)
        new_elevation = map_data.get_value(down_right[1],down_right[0])
        if new_elevation is not None:
            new_moves[down_right] = abs(curr_elevation-new_elevation)
        right_move = sorted(new_moves.items(),key=lambda move: move[1])[0][0]
        self.total_delta += new_moves[right_move]
        return right_move

    def get_total_delta(self):
        return self.total_delta


            # move_deltas = {}
            # current_elevation = self.map_data.get_value(self.curr_pos)

            # up_right_tup = (self.curr_column()+1,self.curr_row()+1)
            # right_tup = (self.curr_column()+1,self.curr_row())
            # down_right_tup = (self.curr_column()+1,self.curr_row()-1)

            # move_delats[up_right] = self.map_data.get_value(up_right)
            # right = self.map_data.get_value()
            # down_right = self.map_data.get_value()


    
    def curr_column(self):
        return self.curr_pos[0]

    def curr_row(self):
        return self.curr_pos[1]





file = "elevation_small.txt"
map_data = MapData(read_file(file))
map_image = MapImage(map_data)
pathfinder = Pathfinder(map_data,map_image)
best_delta = None
best_y = 0
for y in range(map_data.get_length()):
    pathfinder.set_start(0,y)
    pathfinder.find_greedy_path()
    if best_delta is None or pathfinder.get_total_delta() < best_delta:
        best_delta = pathfinder.get_total_delta()
        best_y = y
pathfinder.set_start(0, best_y)
pathfinder.find_greedy_path("purple")
map_image.show()
map_image.save("friday_night_path.png")



# file = input("Which file shall I use? ")
# print(map_data.get_grayscale_value(400,400))



# print((two_d_elev_list))
# print(len(two_d_elev_list))
# print(len(two_d_elev_list[0]))
