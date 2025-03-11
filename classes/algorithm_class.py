
import numpy as np 
import cv2 


class algorithm:
    def __init__(self):
        self.current_node = 0 
        self.arrivialthresh = 15
        self.node_number = 100
        self.radius_scale = 5
        self.freq = 40


    def make_path(self, frame):

     

        video_width = 2048
        video_height = 2448


        center_x = video_width // 2
        center_y = video_height // 2
        radius = min(video_width, video_height) // self.radius_scale  # Assume circle fits within a quarter of the image
        
        coordinates = []
        for i in range(self.node_number):
            theta = 2 * np.pi * i / self.node_number
            x = center_x + int(radius * np.cos(theta))
            y = center_y + int(radius * np.sin(theta))
            coordinates.append((x, y))
        
        coordinates.append(coordinates[0])
        
        pts = np.array(coordinates, np.int32)
        cv2.polylines(frame, [pts], False, (0,0,0), 4)
        
        
        #self.tracker.robot_list[-1].trajectory = coordinates 

        return frame, coordinates


    def run(self, robot_list, frame):
        """
        input: data about robot. eg, velocity or position
        output: magnetic field action commands
        """
        
        
        #input:  robot_list which stores all the attributes for each robot you select
        for bot_num in range(len(robot_list)):
            robot = robot_list[bot_num]
            pos = robot.position_list[-1]
            print("robot {} pos = {}".format(bot_num, pos))



        # make circle 
        frame, coordinates = self.make_path(frame)
        


        

        #define target coordinate
        targetx = coordinates[self.current_node][0]
        targety = coordinates[self.current_node][1]

        #define robots current position
        robotx = robot_list[-1].position_list[-1][0]
        roboty = robot_list[-1].position_list[-1][1]
        
        #calculate error between node and robot
        direction_vec = [targetx - robotx, targety - roboty]
        error = np.sqrt(direction_vec[0] ** 2 + direction_vec[1] ** 2)
        self.alpha = np.arctan2(-direction_vec[1], direction_vec[0])

        if error < self.arrivialthresh:
            self.current_node += 1
        
        #if we reach the end, start over the current_node at 0
        if self.current_node == len(coordinates):
            print("back at beginning")
        






                
        
        
        
        
        #output: actions which is the magetnic field commands applied to the arduino

        Bx = 1 #-1 -> 1
        By = 0 #-1 -> 1
        Bz = 0 #-1 -> 1
        alpha = self.alpha 
        gamma = 90 #0 -> 180 deg
        freq = self.freq #0 -> 180 Hz
        psi = 0 #0 -> 90 deg
        gradient = 1 # gradient has to be 1 for the gradient thing to work
        acoustic_freq = 0
        
        
        return Bx, By, Bz, alpha, gamma, freq, psi, gradient, acoustic_freq, frame