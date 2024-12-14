The tenScan.py file is utilized to detect if there is a change in polar coordinates around a YD-LiDAR to determine if a person has entered the space. 
The LIDARdata.txt and NewLidardata.txt files hold different data inputs from the YD-LiDAR and compares them live within tenScan.py. PyLidar3 is a library required to run tenScan.py.
At default, the tenScan.py is set to only do ten scans for testing purposes but this number can be changed to infinetly scan the space. 
