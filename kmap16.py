from group import Group

"""
4x4 Kavanaugh Map. Contains functions geared towards the ultimate goal
of producing a simplified Boolean Algebra equation by using the Kavanaugh
map method. 
"""
class Kmap16:

    """
    Creates a 4x4 kmap for the class and it's corresponding canonical
    representation. Capital letters are 1. Lowercase are 0.
    
    Also creates F which is a list of all groups, and list_of_f_coords which contains the 
    coordinates of all the groups in F. Both Initalized in the start() function
    """
    def __init__(self):
        #print('Debugging Info')
        self.K = [      
            [0,0,0,0], 
            [0,0,0,0], 
            [0,0,0,0], 
            [0,0,0,0]] 
            
            
        self.M = [
            ["abcd","abcD","abCD","abCd"],
            ["aBcd","aBcD","aBCD","aBCd"],
            ["ABcd","ABcD","ABCD","ABCd"],
            ["Abcd","AbcD","AbCD","AbCd"]]
            
        self.F = []
        self.list_of_f_coords = []
        
    """
    Initalizes the essential start up methods and lists needed
    for the other methods to function.
    """
    def start(self):
        
        adjacent = []
        for row in range(4):
            for col in range(4):
                value = self.K[row][col]
                if value == 1:
                    g = Group(1, (row, col))
                    self.F.append(g)
        
        for group in self.F:
            self.list_of_f_coords.append(group.coord_list)
        
        #print("COORDS OF EACH GROUP IN K")
        #for coord in self.list_of_f_coords:
        #    print(coord)
        
        """
        Nested inside start, gathers the coordinates left, right, up , and down for each group.
        """
        def get_adjacent_groups(): 
            for group in self.F:
                coords = group.get_adjacent_coords()
                adjacent.append(coords)
                
        get_adjacent_groups()
        
        """
        Nested inside start, analyzes the groups in F, and finds groups that are adjacent to each other.
        Appends their coordinates to each groups adjacent_group_coords list
        """
        def analyze_groups():
            for group in self.F:
                gcoords = (group.coord_list[0], group.coord_list[1])
                for alist in adjacent:
                    if gcoords in alist:
                        group.adjacent_groups = group.adjacent_groups+1
                        adjacent_coord = (alist[3][0], alist[0][1])
                        group.adjacent_group_coords.append(adjacent_coord)
                        
        analyze_groups()
        
        # debug print statement
        #print("NUMBER OF ADJACENT COORDS AND THE ADJACENT COORDS")
        #for group in self.F:
        #    print(str(group.adjacent_groups) + " " + str(group.adjacent_group_coords)) 
        
        
    """
    Creates the 8, 4, 2, and 1-boxes from the Kmap unless all or none of the boxes have input. 
    Needed for simplification to work. Returns a list of the simpliest groups that can be created
    in the Kmap
    
    returns: list of Group objects
    """
    def create_boxes(self): 
        if not(len(self.F) == 16 or len(self.F) == 0): 
            allboxes = self.create_8box()
            allboxes = allboxes + self.create_4box(allboxes) 
            allboxes = allboxes + self.create_2box(allboxes)
            allboxes = allboxes + self.create_1box(allboxes)
            #print("ALL CURRENT GROUPS")
            #print(allboxes)
            #print("ALL GROUP COORDS")
            #for group in allboxes:
            #    print("-------------")
            #    print(group.coord_list)
        
            return allboxes
            
    """
    Creates the 8 boxes. 
    
    Returns: a list of 8box Group objects.
    """
    def create_8box(self):
        boxes = self.create_8box_down() + self.create_8box_right()
        print(boxes)
        return boxes
        
    """
    helper function for create_8box
    
    Returns: a list of 8box Group objects
    """
    def create_8box_down(self):
        list_of_new_groups = []
        list_of_columns = []
        list_of_roots = []
        for group in self.F:
            if group.coord_list[0] == 0:
                list_of_roots.append(group)
        
        for group in list_of_roots:
            col = group.coord_list[1]
            temp_list = [group.coord_list]
            num_below = 0
            for i in range(1,4):
                if (i, col) in self.list_of_f_coords:
                    num_below = num_below+1
                    temp_list.append((i,col))
            if num_below == 3:
                list_of_columns.append(temp_list)
                
        
        if len(list_of_columns) >= 2:
            i=0
            while i < len(list_of_columns):
                if self.check_down_column_adjacent(list_of_columns[i], list_of_columns[1]):
                    g = Group(8, list_of_columns[i]+list_of_columns[1])
                    list_of_new_groups.append(g)
                i = i+2
        
        # print("Length of new groups: " + str(len(list_of_new_groups)))
        
        return list_of_new_groups
        
    """
    helper function for create_8box_down, used to compare adjacent columns
    
    Param: l1-column list, l2-column list
    
    Returns: True if both columns are completely next to each other. False if otherwise
    """
    def check_down_column_adjacent(self,l1, l2):
    
        for coord in l1:
            row = coord[0]
            col = coord[1]
            if col < 3:
                right = (row, col+1)
            else:
                right = (row, 0)
                
            if col > 0:
                left = (row, col-1)
            else:
                left = (row, 3)
            
    
            if not(right in l2 or left in l2):
                return False
        return True    
         
    """
    helper function for create_8box
    
    Returns: a list of 8box Group objects
    """
    def create_8box_right(self):
        list_of_new_groups = []
        list_of_columns = []
        list_of_roots = []
        for group in self.F:
            if group.coord_list[1] == 0:
                list_of_roots.append(group)
        
        for group in list_of_roots:
            row = group.coord_list[0]
            temp_list = [group.coord_list]
            num_right = 0
            for i in range(1,4):
                if (row, i) in self.list_of_f_coords:
                    num_right = num_right+1
                    temp_list.append((row, i))
            if num_right == 3:
                list_of_columns.append(temp_list)
                
        
        if len(list_of_columns) >= 2:
            i=0
            while i < len(list_of_columns):
                if self.check_right_column_adjacent(list_of_columns[i], list_of_columns[1]):
                    g = Group(8, list_of_columns[i]+list_of_columns[1])
                    list_of_new_groups.append(g)
                i = i+2
        
        return list_of_new_groups
        
    """
    helper function for create_8box_right, used to compare adjacent rows
    
    Param: l1-row list, l2-row list
    
    Returns: True if they are completely next to each other. False if otherwise
    """
    def check_right_column_adjacent(self,l1, l2):
        for coord in l1:
            row = coord[0]
            col = coord[1]
            left = (row-1, col)
            if row > 0:
                left = (row-1, col)
            else:
                left = (3, col)
            
            if row < 3:
                right = (row+1, col)
            else:
                right = (0, col)
                
            if not(right in l2 or left in l2):
                return False
                
        return True 
    
    """
    Creates the 4 boxes
    
    Param: boxes_list-list of groups of already made boxes
    
    Returns: a list of 4box Group objects
    """
    def create_4box(self,boxes_list):
        boxes = []
        boxes = self.create_4box_down(boxes_list) + self.create_4box_right(boxes_list) + self.create_4box_square(boxes_list)
        return boxes
    
    """
    Helper function
    
    Param: given-tuple(row,col), boxes_list-list of groups of already made boxes
    
    Returns: False if given tuple is in the list of already creates
    boxes, True if not
    """
    def check_not_in_list(self,given, boxes_list): # returns true if not in list, false if in list
        for group in boxes_list:
            if given in group.coord_list:
                return False
        
        return True
    
    """
    Helper function for create_4box
    
    Param: boxes_list-list of groups of already made boxes
    
    Returns: a list of 4box Group objects
    """
    def create_4box_down(self,boxes_list):
        list_of_new_groups=[]
        roots = []
        for group in self.F:
            if group.coord_list[0] == 0: 
                roots.append(group) # ^ instead of doing this to the root, check each individial coord of the 4 box to weed out redundancy
        
        for group in roots:
            row = group.coord_list[0]
            col = group.coord_list[1]
            if self.K[1][col] == 1 and self.K[2][col] == 1 and self.K[3][col] == 1:
                if self.check_not_in_list((1,col), boxes_list) or self.check_not_in_list((2,col), boxes_list) or self.check_not_in_list((3,col), boxes_list):
                    g = Group(4, [(row,col), (1, col), (2,col), (3,col)])
                    list_of_new_groups.append(g)
            
        return list_of_new_groups
    
    """
    Helper function for create_4box
    
    Param: boxes_list-list of groups of already made boxes
    
    Returns: a list of 4boxes Group objects
    """
    def create_4box_right(self,boxes_list):
        list_of_new_groups=[]
        roots = []
        for group in self.F:
            if group.coord_list[1] == 0:
                roots.append(group)
        
        for group in roots:
            row = group.coord_list[0]
            col = group.coord_list[1]
            if self.K[row][1] == 1 and self.K[row][2] == 1 and self.K[row][3] == 1:
                if self.check_not_in_list((row,1), boxes_list) or self.check_not_in_list((row,2), boxes_list) or self.check_not_in_list((row,3), boxes_list):
                    g = Group(4, [(row,col), (row, 1), (row,2), (row,3)])
                    list_of_new_groups.append(g)
        
        return list_of_new_groups
    
    """
    Helper function for create_4box
    
    Param: boxes_list-list of groups of already made boxes
    
    Returns: a list of 4box Group objects
    """
    def create_4box_square(self,boxes_list):
        list_of_new_groups=[]
        roots = []
        for group in self.F:
            if group.adjacent_groups >= 2:
                roots.append(group)
        
        for group in roots:
            row = group.coord_list[0]
            col = group.coord_list[1]
            if self.check_if_square_group(row,col):
                # put a check in place for values to wrap around
                if row < 3:
                    down = (row+1, col)
                else:
                    down = (0, col)
                
                if col < 3:
                    right = (row, col+1)
                else:
                    right = (row, 0)
                
                cross = (down[0], right[1])
                
                if self.check_not_in_list(group.coord_list, boxes_list):
                    g = Group(4, [(row, col), right, down, cross])
                    list_of_new_groups.append(g)
                elif (self.check_not_in_list(right, boxes_list) or self.check_not_in_list(down, boxes_list)) or self.check_not_in_list(cross, boxes_list):
                    g = Group(4, [(row, col), right, down, cross])
                    list_of_new_groups.append(g)
        
        return list_of_new_groups
        
    """
    Helper function for create_4box_square
    
    Param: row-root's row value, col-root's column value
    
    Returns: True if a valid square group can be made from the root's row and col. False if otherwise.
    """
    def check_if_square_group(self,row, col):
        if row < 3:
            down = self.K[row+1][col]
            downT = (row+1, col)
        else:
            down = self.K[0][col]
            downT = (0, col)
            
        if col < 3:
            right = self.K[row][col+1] #right and down are using wrong coords
            rightT = (row, col+1) # redo them for correct result
        else:
            right = self.K[row][0]
            rightT = (row, 0)
        
        # next I need is cross
        cross = self.K[downT[0]][rightT[1]]
        
        if (right == 0):
            return False
            
        if (down == 0):
            return False
            
        if (cross == 0):
            return False
            
        return True
        
    """
    Creates 2 boxes
    
    Param: boxes_list-list of groups of already made boxes
    
    Returns: a list of 2box Group objects
    """
    def create_2box(self,boxes_list):
        boxes = []
        boxes = self.create_2box_down(boxes_list) + self.create_2box_right(boxes_list)
        return boxes
    
    """
    Helper function for create_2box
    
    Param: boxes_list-list of groups of already made boxes
    
    Returns: a list of 2box Group objects
    """
    def create_2box_down(self,boxes_list):
        list_of_new_groups=[]
        roots = []
        for group in self.F:
            if group.adjacent_groups >= 1: # roots can be within a group, as long as one of the boxes are outside the boxes_list
                roots.append(group)
        
        for group in roots:
            row = group.coord_list[0]
            col = group.coord_list[1]
            
            if row < 3:
                down = self.K[row+1][col]
                downT = (row+1, col)
            else:
                down = self.K[0][col]
                downT = (0, col)
            
            if down == 1:
                if self.check_not_in_list((row,col), boxes_list): 
                    g = Group(2, [(row,col), downT])
                    list_of_new_groups.append(g)
                elif self.check_not_in_list(downT, boxes_list): 
                    g = Group(2, [(row,col), downT])
                    list_of_new_groups.append(g)
        
        return list_of_new_groups
    
    """
    Helper function for create_2box
    
    Param: boxes_list-list of groups of already made boxes
    
    Returns: a list of 2box Group objects
    """
    def create_2box_right(self,boxes_list):
        list_of_new_groups=[]
        roots = []
        for group in self.F:
            if group.adjacent_groups >= 1: 
                roots.append(group)
        
        for group in roots:
            row = group.coord_list[0] # 1
            col = group.coord_list[1] # 0
            
            
            if col < 3:
                right = self.K[row][col+1]
                rightT = (row, col+1)
            else:
                right = self.K[row][0]
                rightT = (row, 0)
            
            print("create_2_box_debug, " + str(right) + " current coord: " + str((row, col)))
            if right == 1:
                if self.check_not_in_list((row,col), boxes_list):
                        g = Group(2, [(row,col), rightT])
                        list_of_new_groups.append(g)    
                elif self.check_not_in_list(rightT, boxes_list): # issue might be here as the identification works fine
                        g = Group(2, [(row,col), rightT])
                        list_of_new_groups.append(g)
        
        return list_of_new_groups
    
    """
    Creates 1 boxes 
    
    Param: boxes_list-list of groups of already made boxes
    
    Returns: a list of 1box Group objects
    """
    def create_1box(self,boxes_list):
        list_of_new_groups = []
        for group in self.F:
            if self.check_not_in_list(group.coord_list, boxes_list):
                g = Group(1, [(group.coord_list[0], group.coord_list[1])])
                list_of_new_groups.append(g)
        
        return list_of_new_groups
    
    """
    Creates Canonical Representation equations from the finished list of boxes. 
    
    Param: boxes_list-list of groups of already made boxes
    
    Returns: the list of equations.
    """
    def create_equations_from_boxes(self, boxes_list):
        if not(len(self.F) == 16 or len(self.F) == 0): 
            equations = []
            for box in boxes_list: # each box is a list of groups
                temp_list = []
                for coord in box.coord_list:
                    row = coord[0]
                    col = coord[1]
                    temp_list.append(self.M[row][col])
                equations.append(temp_list)
            
            #print("CANONICAL EQUATIONS")
            #print(equations)
            return equations
    
    """
    Simplifies Canonical equations
    
    Param: equations_list-a list of Canonical Representation of K-Map
    
    Returns: a string of the final simplified equation
    """
    def simplify_equations(self, equations_list):
        if len(self.F) == 16: 
            return "1"
        if len(self.F) == 0: 
            return "0"
        
        simplified_list = []
        final_equation = ""
        for group in equations_list:
            saved = ""
            score = 0
            if len(group) > 1:
                root = group[0]
                for i in range(4):
                    for equation in group:
                        if not(equation == root):
                            if equation[i] == root[i]:
                                score = score + 1
                                if score == len(group)-1:
                                    score = 0
                                    saved = saved + equation[i]
                            else:
                                break
                simplified_list.append(saved)                    
            else:
                simplified_list.append(group[0])
            
            
        
        #print("SIMPLIFIED LIST")
        # remove for defbug info 
        #print("\033c", end="")
        for i in range(len(simplified_list)):
            if i < (len(simplified_list)-1):
                final_equation = final_equation + simplified_list[i] + " + "
            else:
                final_equation = final_equation + simplified_list[i]
            
        #print(simplified_list)
        #print(final_equation)
        return final_equation