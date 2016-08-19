import numpy as np

class Robot(object):
    def __init__(self, maze_dim):
        '''
        Use the initialization function to set up attributes that your robot
        will use to learn and navigate the maze. Some initial attributes are
        provided based on common information, including the size of the maze
        the robot is placed in.
        '''
        self.wall_costs = {'up': [8,1,2],
                            'down': [2,4,8],
                            'left': [4,8,1],
                            'right': [1,2,4]
                            }
        self.bin_index = {'up': [0,3,2],
                            'down': [2,1,0],
                            'left': [1,0,3],
                            'right':  [3,2,1]}
        self.location = [0, 0]
        self.heading = 'up'
        self.maze_dim = maze_dim

        # Initialize all the squares to 15 which indicates no walls
        self.walls = [[15 for i in range(maze_dim)] for j in range(maze_dim)]

        # Initialize all distance to goal as 99
        self.distance_to_goal = [[99 for i in range(maze_dim)] for j in range(maze_dim)]
        self.found_goal = False
        self.wall_updated = [[0 for i in range(maze_dim)] for j in range(maze_dim)]
        self.chosen_goal = [self.maze_dim/2 - 1, self.maze_dim/2]
        self.count = 0

    def check_limits(self, param1):
        if int(param1) >=0 and int(param1) < self.maze_dim:
            return True
        else:
            return False

    def choose_new_goal(self, my_list):
        sorted_list = sorted(my_list,reverse=True)
        chosen_item = sorted_list.pop(0)
        newx=chosen_item[0]
        newy=chosen_item[1]
        #newx = np.random.randint(1,self.maze_dim-1)
        ##newy = np.random.randint(1,self.maze_dim-1)
        #while self.wall_updated[newx][newy] == 1 and np.sum(self.wall_updated) != (int(self.maze_dim)*int(self.maze_dim)):
        #    newx = np.random.randint(1,self.maze_dim-1)
        #    newy = np.random.randint(1,self.maze_dim-1)
        return newx,newy



    def flood_fill(self,xlocation,ylocation):
        moves= [[-1,0], #west
                [0,-1], #south
                [1,0],  #east
                [0,1]   #north
                ]

        self.distance_to_goal[xlocation][ylocation] = 0

        # creating a 2-D array which indicates which indicates all squares have not been traveled to
        traveled = [[0 for i in range(self.maze_dim)] for j in range(self.maze_dim)]

        traveled[xlocation][ylocation] = 1

        next_list = [[xlocation,ylocation]]

        while len(next_list)>0:
            current = next_list.pop(0)
            binary_wall = np.binary_repr(self.walls[current[0]][current[1]],width=4)
            for i in range(len(binary_wall)):
                if int(binary_wall[i]) == 1:
                    next_move = [(current[0]+moves[i][0]),(current[1]+moves[i][1])]
                    if (next_move[0]>=0 and next_move[0]<self.maze_dim and next_move[1]>=0 and next_move[1]<self.maze_dim):
                        if (traveled[next_move[0]][next_move[1]] != 1):
                            self.distance_to_goal[next_move[0]][next_move[1]] = self.distance_to_goal[current[0]][current[1]] + 1
                            next_list.append(next_move)
                            traveled[next_move[0]][next_move[1]] = 1

    def sense_wall(self, direction, sense):
        if direction == 'up':
            xparam1 = -1
            xparam2 = 0 
            xparam3 = 1
            yparam1 = 0
            yparam2 = 1
            yparam3 = 0
            opposite = 'down'
            add_param1 = 1
            add_param2 = 0
        if direction == 'down':
            xparam1 = 1
            xparam2 = 0 
            xparam3 = -1
            yparam1 = 0
            yparam2 = -1
            yparam3 = 0
            opposite = 'up'
            add_param1 = -1
            add_param2 = 0
        if direction == 'left':
            xparam1 = 0
            xparam2 = -1 
            xparam3 = 0
            yparam1 = -1
            yparam2 = 0
            yparam3 = 1
            opposite = 'right'
            add_param1 = 0
            add_param2 = 1
        if direction == 'right':
            xparam1 = 0
            xparam2 = 1 
            xparam3 = 0
            yparam1 = 1
            yparam2 = 0
            yparam3 = -1
            opposite = 'left'
            add_param1 = 0
            add_param2 = -1

        left_sq_loc = self.walls[self.location[0]+xparam1*sense[0]][self.location[1]+yparam1*sense[0]]
        front_sq_loc = self.walls[self.location[0]+xparam2*sense[1]][self.location[1]+yparam2*sense[1]]
        right_sq_loc = self.walls[self.location[0]+xparam3*sense[2]][self.location[1]+yparam3*sense[2]]

        left_add_x = self.location[0]+xparam1*sense[0]-add_param1
        left_add_y = self.location[1]+yparam1*sense[0]-add_param2
        front_add_x = self.location[0]+xparam2*sense[1]-add_param2
        front_add_y = self.location[1]+yparam2*sense[1]+add_param1
        right_add_x = self.location[0]+xparam3*sense[2]+add_param1
        right_add_y = self.location[1]+yparam3*sense[2]+add_param2

        if self.check_limits(left_add_x) and self.check_limits(left_add_y):
            left_sq_plus_loc = self.walls[left_add_x][left_add_y]
        if self.check_limits(front_add_x) and self.check_limits(front_add_y):
            front_sq_plus_loc = self.walls[front_add_x][front_add_y]
        if self.check_limits(right_add_x) and self.check_limits(right_add_y):
            right_sq_plus_loc = self.walls[right_add_x][right_add_y]

        far_left_walls = np.binary_repr(left_sq_loc, width=4)
        far_front_walls = np.binary_repr(front_sq_loc, width=4)
        far_right_walls = np.binary_repr(right_sq_loc, width=4)

        if int(far_left_walls[self.bin_index[direction][0]]) == 1:
            self.walls[self.location[0]+xparam1*sense[0]][self.location[1]+yparam1*sense[0]] -= self.wall_costs[direction][0]
            self.wall_updated[self.location[0]+xparam1*sense[0]][self.location[1]+yparam1*sense[0]] = 1
            print "modified wall left of what u r facing\n"
            print "["+str(self.location[0]+xparam1*sense[0])+","+str(self.location[1]+yparam1*sense[0])+"]"
            if self.check_limits(left_add_x) and self.check_limits(left_add_y):
                print "additional left updated"
                self.walls[left_add_x][left_add_y] -= self.wall_costs[opposite][0]
                self.wall_updated[left_add_x][left_add_y] = 1

        if int(far_front_walls[self.bin_index[direction][1]]) == 1:
            self.walls[self.location[0]+xparam2*sense[1]][self.location[1]+yparam2*sense[1]] -= self.wall_costs[direction][1]
            self.wall_updated[self.location[0]+xparam2*sense[1]][self.location[1]+yparam2*sense[1]] = 1
            print "modified wall in front of what u are facing\n"
            print "["+str(self.location[0]+xparam2*sense[1])+","+str(self.location[1]+yparam2*sense[1])+"]"
            if self.check_limits(front_add_x) and self.check_limits(front_add_y):
                print "additional front updated"
                self.walls[front_add_x][front_add_y] -= self.wall_costs[opposite][1]
                self.wall_updated[front_add_x][front_add_y] = 1

        if int(far_right_walls[self.bin_index[direction][2]]) == 1:
            self.walls[self.location[0]+xparam3*sense[2]][self.location[1]+yparam3*sense[2]] -= self.wall_costs[direction][2]
            self.wall_updated[self.location[0]+xparam3*sense[2]][self.location[1]+yparam3*sense[2]] = 1
            print "modified wall right of what you are facing\n"
            print "["+str(self.location[0]+xparam3*sense[2])+","+str(self.location[1]+yparam3*sense[2])+"]"
            if self.check_limits(right_add_x) and self.check_limits(right_add_y):
                print "additoinal right updated"
                self.walls[right_add_x][right_add_y] -= self.wall_costs[opposite][2]
                self.wall_updated[right_add_x][right_add_y] = 1



    def next_move(self, sensors):
        '''
        Use this function to determine the next move the robot should make,
        based on the input from the sensors after its previous move. Sensor
        inputs are a list of three distances from the robot's left, front, and
        right-facing sensors, in that order.
        Outputs should be a tuple of two values. The first value indicates
        robot rotation (if any), as a number: 0 for no rotation, +90 for a
        90-degree rotation clockwise, and -90 for a 90-degree rotation
        counterclockwise. Other values will result in no rotation. The second
        value indicates robot movement, and the robot will attempt to move the
        number of indicated squares: a positive number indicates forwards
        movement, while a negative number indicates backwards movement. The
        robot may move a maximum of three units per turn. Any excess movement
        is ignored.
        If the robot wants to end a run (e.g. during the first training run in
        the maze) then returing the tuple ('Reset', 'Reset') will indicate to
        the tester to end the run and return the robot to the start.
        '''
        self.count += 1
        print "\n-------------- new run -------------\n"
        print self.count

        # Definining the goal locations for the flood fill algorithm
        already_moved = False
        goal_a = [(self.maze_dim-1)/2,(self.maze_dim-1)/2]
        goal_b = [(self.maze_dim-1)/2,(self.maze_dim)/2]
        goal_c = [(self.maze_dim)/2,(self.maze_dim-1)/2]
        goal_d = [(self.maze_dim)/2,(self.maze_dim)/2]

        goal_e = [self.maze_dim/2 - 1, self.maze_dim/2]

        headings = ['up', 'right', 'down', 'left']

        # update walls
        # note that I had to invert the north and south since the array is facing opposite direction
        # converting the current wall status into a binary form
        if self.heading == 'up':
            self.sense_wall('up', sensors)
        if self.heading == 'down':
            self.sense_wall('down', sensors)
        if self.heading =='left':
            self.sense_wall('left', sensors)
        if self.heading =='right':
            self.sense_wall('right', sensors)

        wall_bin_updated = np.binary_repr(self.walls[self.location[0]][self.location[1]], width=4)
        west_wall_updated = int(wall_bin_updated[0])
        south_wall_updated = int(wall_bin_updated[1])
        east_wall_updated = int(wall_bin_updated[2])
        north_wall_updated = int(wall_bin_updated[3])
        if self.location == self.chosen_goal:
            self.found_goal = True

        new_list = []
        if self.found_goal == False:
            self.flood_fill(self.chosen_goal[0], self.chosen_goal[1])
        else:
            for i in range(len(self.wall_updated)):
                for j in range(len(self.wall_updated)):
                    if self.wall_updated[i][j] == 0:
                        print [i,j]
                        new_list.append([i,j])
            if len(new_list) > 0:
                newx,newy=self.choose_new_goal(new_list)
                self.chosen_goal = [newx,newy]
                self.flood_fill(self.chosen_goal[0],self.chosen_goal[1])
                self.found_goal == False
            else:
                print "done"

        # Directions on where to move after calculating new distances to goal
        r_moves = [[-1,0],
                    [0,-1],
                    [1,0],
                    [0,1]]

        move_list = []
        dist_list = []

        if self.heading == 'up' and not already_moved:
            print "hi i am in up section"
            if self.location[1] >= 0 and self.location[1] < self.maze_dim:
                for i in range(len(wall_bin_updated)):
                    if int(wall_bin_updated[i]) == 1:
                        movex = (self.location[0]+r_moves[i][0])
                        movey = (self.location[1]+r_moves[i][1])
                        if (movex>=0 and movex<self.maze_dim and movey>=0 and movey<self.maze_dim):
                            move_list.append([movex,movey])
                            dist_list.append(self.distance_to_goal[movex][movey])
                    if len(move_list) >0:
                        chosen_move = move_list[np.argmin(dist_list)]
                deltax = chosen_move[0]-self.location[0]
                deltay = chosen_move[1]-self.location[1]

                if deltax == 0 and deltay == 1:
                    rotation = 0
                    movement = 1

                if deltax == 1 and deltay == 0:
                    rotation = 90
                    movement = 1
                    self.heading = 'right'
                #if deltax == 0 and deltay == -1:
                #    movement = -1
                #    rotation = 0
                if deltax == 0 and deltay == -1:
                    rotation = 90
                    movement = 0
                    self.heading = 'right'
                    
                if deltax == -1 and deltay == 0:
                    rotation = -90
                    movement = 1
                    self.heading = 'left'

                already_moved = True

        if self.heading == 'down' and not already_moved:
            if self.location[1] >=0 and self.location[1] < self.maze_dim:
                for i in range(len(wall_bin_updated)):
                    if int(wall_bin_updated[i]) == 1:
                        movex = (self.location[0]+r_moves[i][0])
                        movey = (self.location[1]+r_moves[i][1])
                        if (movex>=0 and movex<self.maze_dim and movey>=0 and movey<self.maze_dim):
                            move_list.append([movex,movey])
                            dist_list.append(self.distance_to_goal[movex][movey])

                    if len(move_list) >0:
                        chosen_move = move_list[np.argmin(dist_list)]

                deltax = chosen_move[0]-self.location[0]
                deltay = chosen_move[1]-self.location[1]

                #if deltax == 0 and deltay == 1:
                #    movement = -1
                #    rotation = 0
                if deltax == 0 and deltay == 1:
                    rotation = -90
                    movement = 0
                    self.wall_updated[self.location[0]][self.location[1]] = 1
                    self.heading = 'right'
                if deltax == 1 and deltay == 0:
                    rotation = -90
                    movement = 1
                    self.heading = 'right'
                if deltax == 0 and deltay == -1:
                    rotation = 0
                    movement = 1
                if deltax == -1 and deltay == 0:
                    rotation = 90
                    movement = 1
                    self.heading = 'left'

                already_moved = True

        if self.heading == 'left' and not already_moved:
            if self.location[0] >= 0 and self.location[0] < self.maze_dim:
                for i in range(len(wall_bin_updated)):
                    if int(wall_bin_updated[i]) == 1:
                        movex = (self.location[0]+r_moves[i][0])
                        movey = (self.location[1]+r_moves[i][1])
                        if (movex>=0 and movex<self.maze_dim and movey>=0 and movey<self.maze_dim):
                            move_list.append([movex,movey])
                            dist_list.append(self.distance_to_goal[movex][movey])
                    if len(move_list) >0:
                        chosen_move = move_list[np.argmin(dist_list)]

                deltax = chosen_move[0]-self.location[0]
                deltay = chosen_move[1]-self.location[1]

                if deltax == 0 and deltay == 1:
                    rotation = 90
                    movement = 1
                    self.heading = 'up'
                #if deltax == 1 and deltay == 0:
                #    rotation = 0
                #    movement = -1
                if deltax == 1 and deltay == 0:
                    rotation = 90
                    movement = 0
                    self.wall_updated[self.location[0]][self.location[1]] = 1
                    self.heading = 'up'
                if deltax == 0 and deltay == -1:
                    rotation = -90
                    movement = 1
                    self.heading = 'down'
                if deltax == -1 and deltay == 0:
                    rotation = 0
                    movement = 1

                already_moved = True

        if self.heading == 'right' and not already_moved:
            if self.location[0] >=0 and self.location[0] < self.maze_dim:
                for i in range(len(wall_bin_updated)):
                    if int(wall_bin_updated[i]) == 1:
                        movex = (self.location[0]+r_moves[i][0])
                        movey = (self.location[1]+r_moves[i][1])
                        if (movex>=0 and movex<self.maze_dim and movey>=0 and movey<self.maze_dim):
                            move_list.append([movex,movey])
                            dist_list.append(self.distance_to_goal[movex][movey])

                    if len(move_list) >0:
                        chosen_move = move_list[np.argmin(dist_list)]

                deltax = chosen_move[0]-self.location[0]
                deltay = chosen_move[1]-self.location[1]

                if deltax == 0 and deltay == 1:
                    rotation = -90
                    movement = 1
                    self.heading = 'up'
                if deltax == 1 and deltay == 0:
                    rotation = 0
                    movement = 1
                if deltax == 0 and deltay == -1:
                    rotation = 90
                    movement = 1
                    self.heading = 'down'
                #if deltax == -1 and deltay == 0:
                #    rotation = 0
                #    movement = -1
                if deltax == -1 and deltay == 0:
                    rotation = -90
                    movement = 0
                    self.wall_updated[self.location[0]][self.location[1]] = 1
                    self.heading = 'up'
                already_moved = True

        #################### debug purposes ######################
        print "\n"
        print "\n"

        print "updated walls"
        for item in self.wall_updated:
            print item
        
        print "distances"
        for item in self.distance_to_goal:
            print item
        print "\n wallz"
        for item in self.walls:
            print item
        print "\nsensors"
        print sensors
        print "\n" 

        print "wall binary"
        print wall_bin_updated
        print "check location 3,3"
        print np.binary_repr(self.walls[3][3], width=4)
        print "\n"

        print "heading:"
        print self.heading
        print "\n"
        print "location"
        if movement == 1:
            self.location = chosen_move
        print self.location

        print "\n"

        # finally we set the goal back to it's intended location
        if self.count == 1000:
            # closing all the unsearched openings incase they are fake openings


            self.flood_fill(self.maze_dim/2 - 1, self.maze_dim/2)
            print "final distances"
            for item in self.distance_to_goal:
                print item
            print "\n final wallz"
            for item in self.walls:
                print item

        return rotation, movement
