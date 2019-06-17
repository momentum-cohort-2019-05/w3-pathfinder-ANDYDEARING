from PIL import Image, ImageColor
import random
import argparse

def read_asc_file(file):
    """reads a file in asc format"""
    with open(file) as source_file:
            source_str = source_file.read()
            source_str = source_str.split()

    # read the correct rows and columns from .asc format
    num_cols = int(source_str[1])
    num_rows = int(source_str[3])

    source_two_d_list = []

    # start reading at index 10 per .asc format
    index = 10
    
    for _ in range(num_rows):
        # empty for the new row
        row = []
        for _ in range(num_cols):
            # make a row list
            row.append(int(source_str[index]))
            index += 1
        # append that list
        source_two_d_list.append(row)
    
    return source_two_d_list

def read_file(file):
    # get the file format, if .txt run here
    if file[len(file)-4:] == ".txt":
        with open(file) as source_file:
            source_str = source_file.read()
            source_str = source_str.split("\n")
    
        source_two_d_list = []

        for line in source_str:
            # I don't know why I'm getting empty lists, but I can clean them out
            if line.split() != []:
                source_two_d_list.append([int(_) for _ in line.split()])

    elif file[len(file)-4:] == ".asc":
        # otherwise run .asc function
        source_two_d_list = read_asc_file(file)

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
        self.path_record = []
    
    def set_start(self, coord_x_y):
        """resets the starting position to the passed coordinates
        and total_delta to 0, takes an (x,y) tuple"""
        self.curr_pos = (coord_x_y[0], coord_x_y[1])
        self.total_delta = 0
        self.path_record = []
        return None

    def get_x(self):
        return self.curr_pos[0]

    def get_y(self):
        return self.curr_pos[1]

    def out_of_bounds(self):
        """returns a tuple with an out of bounds value"""
        return ( self.map_data.get_width(), self.map_data.get_length() )

    def get_greedy_potenitals(self):
        """returns the next 3 coord tuples for greedy in the
        order: up_right, right, down_right"""
        # if the y position is not at the top or the bottom
        # return all three poitentials
        if self.map_data.get_length()-1 > self.get_y() > 0:
            return (self.get_x()+1,self.get_y()+1),(self.get_x()+1, self.get_y()),(self.get_x()+1, self.get_y()-1)
        # otherise return forward and down_right at the top
        elif self.get_y() == 0:
            return (self.get_x()+1,self.get_y()+1) , (self.get_x()+1, self.get_y()), self.out_of_bounds()
        # or forward and up right at the bottom
        else: 
            return self.out_of_bounds(), (self.get_x()+1, self.get_y()), (self.get_x()+1, self.get_y()-1)

    def find_greedy_path(self, color="cyan"):
        """finds the path by the greedy algorithm"""
        # draw the starting point
        self.map_image.putpixel(self.curr_pos)
        # move from left to right via the greedy algorithm
        for _ in range(self.map_data.get_width()-self.get_x()-1):
            # breakpoint()
            down_right, right, up_right = self.get_greedy_potenitals()
            next_move_tup = self.get_greedy_move(up_right, right, down_right)
            self.curr_pos = next_move_tup
            self.map_image.putpixel(self.curr_pos, color)

    def get_greedy_move(self, down_right, right, up_right):
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
        right_move_list = sorted(new_moves.items(),key=lambda move: move[1])
        # if there's a tie
        if right_move_list[0][1]==right_move_list[1][1]:
        # and it's a three way tie
            if len(right_move_list) == 3 and right_move_list[0][1]==right_move_list[2][1]:
                right_move = right_move_list[random.randint(0,2)][0]
            # otherwise flip a coin
            else:
                right_move = right_move_list[random.randint(0,1)][0]
        # or choose the winner if it's clear
        else:
            right_move = right_move_list[0][0]

        self.total_delta += new_moves[right_move]
        self.path_record.append(right_move)
        # debug
        if right_move[1] < 0:
            breakpoint()
        return right_move

    def get_total_delta(self):
        """returns the total elevation change"""
        return self.total_delta

    def get_path_record(self):
        """returns the path record list of (x,y) tuples"""
        return self.path_record

    def retrace_path(self, path_list, color="blue"):
        """retraces a line by a list of tuples"""
        for coord in path_list:
            self.map_image.putpixel(coord, color)
        return None

    def find_greedy_river(self, direction, start_pt=self.curr_pos):
        

def get_file_and_colors():
    """gets the file path and colors from the terminal
    returning file path, path_color, and best_color"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", default="elevation_small.txt",
    help="choose the file you want to open")
    parser.add_argument("-bc", "--bestcolor", default="red",
    help="choose the color of the best path displayed")
    parser.add_argument("-pc", "--pathcolor", default="cyan",
    help="choose the color of the paths displayed")
    args = parser.parse_args()
    file = args.file
    path_color = args.pathcolor
    best_color = args.bestcolor
    return file, args.pathcolor, args.bestcolor

def main():
    file, path_color, best_color = get_file_and_colors()

    try:
        map_data = MapData(read_file(file))
    except:
        print("File not found.")
        exit()

    # open the file and build the map objecs
    map_data = MapData(read_file(file))
    map_image = MapImage(map_data)
    pathfinder = Pathfinder(map_data,map_image)

    # make a path for every y coordinate, recording them
    delta_paths = {}
    for y in range(map_data.get_length()):
        pathfinder.set_start((0,y))
        pathfinder.find_greedy_path(path_color)
        delta_paths[pathfinder.get_total_delta()] = pathfinder.get_path_record()

    # sort them and choose the smallest delta
    best_path = sorted(delta_paths.items(),key=lambda delta: delta[0])[0][1]

    # redraw that line in user color, red by default
    pathfinder.retrace_path(best_path, best_color)
    map_image.show()

def advanced():
    file, path_color, best_color = get_file_and_colors()

    try:
        map_data = MapData(read_file(file))
    except:
        print("File not found.")
        exit()

    # open the file and build the map objecs
    map_data = MapData(read_file(file))
    map_image = MapImage(map_data)
    pathfinder = Pathfinder(map_data,map_image)

    # start in the middle
    start_tup = (int(map_data.get_width()/2),int(map_data.get_length()/2))
    pathfinder.set_start(start_tup)
    pathfinder.find_greedy_river("right")
    pathfinder.find_greedy_river("left", start_tup)

    # find path going right


if __name__ == "__main__":
    # main()
    advanced()
