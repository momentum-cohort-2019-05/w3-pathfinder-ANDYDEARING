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
    """class to hold topographical data for a map"""
    def __init__(self, data_file):
        """expects data_file as a 2d list of int elevations
        min and max value required to set color gradients"""
        self.data_file = data_file
        self.max_value = self.get_max()
        self.min_value = self.get_min()

    def get_width(self):
        """return the number of columns"""
        return len(self.data_file[0])

    def get_length(self):
        """return the number of rows"""
        return len(self.data_file)

    def get_grayscale_value(self, coord_x_y):
        """distrubtes 256 shades of gray over the range of data using
        max and min values, takes an x,y tuple returns an int for the
         gray of the point requested"""
        gray_value = (self.max_value - self.min_value) / 256
        return int((self.data_file[coord_x_y[1]][coord_x_y[0]]-self.min_value) / gray_value)

    def get_min(self):
        """returns the minimum value of the data_file"""
        list_of_mins = []
        for row in self.data_file:
            list_of_mins.append(min(row))
        return min(list_of_mins)

    def get_max(self):
        """returns the maximum value of the data_file"""
        list_of_maxes = []
        for row in self.data_file:
            list_of_maxes.append(max(row))
        return max(list_of_maxes)

    def get_value(self, coord_x_y):
        """takes a coord_x_y tuple and returns the elevation
        value, returning None if not found"""
        try:
            return self.data_file[coord_x_y[1]][coord_x_y[0]]
        except:
            return None

class MapImage:
    """class to hold map images generated from MapData"""
    def __init__(self, map_data):
        """build the map image in grayscale from the data"""
        self.map_data = map_data
        self.image = self.build_image()
    
    def show(self):
        """displays the MapImage"""
        self.image.show()

    def build_image(self):
        """builds the image in RGBA format, grayscale"""
        img = Image.new('RGBA', (self.map_data.get_width(), self.map_data.get_length()) )
        for x in range(self.map_data.get_width()):
            for y in range(self.map_data.get_length()):
                gray_value = self.map_data.get_grayscale_value((x,y))
                img.putpixel((x,y), (gray_value,gray_value,gray_value,255))
        return img
    
    def putpixel(self, column_row_tup, color="red"):
        """for drawing paths, defaults to red"""
        self.image.putpixel(column_row_tup,ImageColor.getcolor(color, "RGBA"))
        return None
    
    def save(self, path):
        """saves the image file to the passed path"""
        self.image.save(path)
        return None

class Pathfinder:
    def __init__(self, map_data, map_image):
        """loads a MapData, MapImage, and defaults"""
        self.map_data = map_data
        self.map_image = map_image
        self.curr_pos = (0,0)
        self.total_delta = 0
    
    def set_start(self, coord_x_y):
        """resets the starting position to the passed coordinates
        and total_delta to 0, takes an (x,y) tuple"""
        self.curr_pos = (coord_x_y[0], coord_x_y[1])
        self.total_delta = 0
        return None

    def get_x(self):
        return self.curr_pos[0]

    def get_y(self):
        return self.curr_pos[1]

    def get_greedy_potenitals(self):
        """returns the next 3 coord tuples for greedy in the
        order: up_right, right, down_right"""
        return (self.get_x()+1,self.get_y()+1), (self.get_x()+1, self.get_y()), (self.get_x()+1, self.get_y()-1)

    def find_greedy_path(self, color="cyan"):
        """finds the path by the greedy algorithm"""
        # draw the starting point
        self.map_image.putpixel(self.curr_pos)
        # move from left to right via the greedy algorithm
        for _ in range(self.map_data.get_width()-self.get_x()-1):
            up_right, right, down_right = self.get_greedy_potenitals()
            next_move_tup = self.get_greedy_move(up_right, right, down_right)
            self.curr_pos = next_move_tup
            self.map_image.putpixel(self.curr_pos, color)

    def get_greedy_move(self, up_right, right, down_right):
        """recieves three tuples of (x,y) data (potentially None) and
        selects the best move by the greedy algorithm, returning a (column,row)
        tuple"""
        curr_elevation = self.map_data.get_value(self.curr_pos)
        new_moves = {}
        new_elevation = self.map_data.get_value(up_right)
        if new_elevation is not None:
            new_moves[up_right] = abs(curr_elevation-new_elevation)
        new_elevation = self.map_data.get_value(right)
        if new_elevation is not None:
            new_moves[right] = abs(curr_elevation-new_elevation)
        new_elevation = self.map_data.get_value(down_right)
        if new_elevation is not None:
            new_moves[down_right] = abs(curr_elevation-new_elevation)
        right_move = sorted(new_moves.items(),key=lambda move: move[1])[0][0]
        self.total_delta += new_moves[right_move]
        return right_move

    def get_total_delta(self):
        return self.total_delta

# def best_greedy_path():




file = "elevation_large.txt"
map_data = MapData(read_file(file))
map_image = MapImage(map_data)
pathfinder = Pathfinder(map_data,map_image)
deltas = {}
for y in range(map_data.get_length()):
    pathfinder.set_start((0,y))
    pathfinder.find_greedy_path()
    deltas[y] = pathfinder.get_total_delta()
# breakpoint()
best_y = sorted(deltas.items(),key=lambda delta: delta[1])[0][0]
pathfinder.set_start((0,best_y))
pathfinder.find_greedy_path("lightgreen")
map_image.show()
# map_image.save("friday_night_path2.png")
