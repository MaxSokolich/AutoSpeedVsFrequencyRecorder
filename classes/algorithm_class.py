
import numpy as np 
import cv2 


class algorithm:
    def __init__(self):
        self.counter = 0
        self.current_node = 0 
        self.arrivialthresh = 15
        self.node_number = 100
        self.radius_scale = 5
        self.freq = 0
        self.freq_interval = 100
        self.freq_increment = 1


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
        # make circle 
        frame, target_coordinates = self.make_path(frame)
        
        if len(robot_list) > 0:
            #input:  robot_list which stores all the attributes for each robot you select

          
            pos = robot_list[-1].position_list[-1]
                

            #define target coordinate
            targetx = target_coordinates[self.current_node][0]
            targety = target_coordinates[self.current_node][1]

            #define robots current position
            robotx = pos[0]
            roboty = pos[1]
            
            #calculate error between node and robot
            direction_vec = [targetx - robotx, targety - roboty]
            error = np.sqrt(direction_vec[0] ** 2 + direction_vec[1] ** 2)
          
            self.alpha = np.arctan2(-direction_vec[1], direction_vec[0])
            cv2.arrowedLine(
                    frame,
                    (int(robotx), int(roboty)),
                    (int(targetx), int(targety)),
                    [0, 0, 0],
                    3,
                )
            cv2.putText(frame,"node = {}/{}".format(self.current_node, len(target_coordinates)),
                    (int(2000),int(200)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1, 
                    thickness=4,
                    color = (255, 255, 255))
            

            if error < self.arrivialthresh:
                self.current_node += 1

        
            #if we reach the end, start over the current_node at 0
            if self.current_node == len(target_coordinates):
                self.current_node = 0

            #every 40 freq_counter frames incriment the frequency
            if self.counter % self.freq_interval == 0:
                self.freq += self.freq_increment


            

        #output: actions which is the magetnic field commands applied to the arduino

        Bx = 0 #-1 -> 1
        By = 0 #-1 -> 1
        Bz = 0 #-1 -> 1
        alpha = self.alpha - np.pi/2 
        gamma = np.pi/2 #0 -> 180 deg
        freq = self.freq #0 -> 180 Hz
        psi = np.pi/2 #0 -> 90 deg
        gradient = 0 
        acoustic_freq = 0
        
        self.counter +=1
        cv2.putText(frame,"counter = {}".format(self.counter),
                    (int(2000),int(400)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1, 
                    thickness=4,
                    color = (255, 255, 255))

        return Bx, By, Bz, alpha, gamma, freq, psi, gradient, acoustic_freq, frame