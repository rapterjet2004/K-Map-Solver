"""
A class used to represent a single grouping of coordinates in a Kavanaugh
Map. Each Group has a size, a list of coordinates inside, adjacent groups, and 
the coordinates of the adjacent groups
"""
class Group:
    
    """
    Creates the global variables
    """
    def __init__(self, size, coord_list):
        self.size = size
        self.coord_list = coord_list
        self.adjacent_groups = 0
        self.adjacent_group_coords = []
    
    
    """
    Gets the adjacent coordinates to this Group. Only called
    if size equals 1
    
    Returns: Tuple(left,right,up,down) adjacent coords
    """
    def get_adjacent_coords(self):
        if self.size == 1:
            row = self.coord_list[0]
            col = self.coord_list[1]
            
            if row > 0:
                left = (row-1, col)
            else:
                left = (3, col)
                
            if col > 0:
                down = (row, col-1)
            else:
                down = (row, 3)
                
            if row < 3:
                right = (row+1, col)
            else:
                right = (0, col)
            
            if col < 3:
                up = (row, col+1)
            else:
                up = (row, 0)
                
            return [left, right, up, down]