import PyLidar3
import matplotlib.pyplot as plt
import numpy as np

#Serial port to which lidar connected, Get it from device manager windows
#In linux type in terminal -- ls /dev/tty* 
port = "COM4" #windows
#port = "/dev/ttyUSB0" #linux
Obj = PyLidar3.YdLidarX4(port) #PyLidar3.your_version_of_lidar(port,chunk_size) 



lst1= [] #holds the information of the very first scan
lst2= [] #holds the newest 360 values to be compared to the initial data


filename = 'LIDARdata.txt' #sets variable to put initial data into a text file
filename2= 'NewLidardata.txt' #sets variable to put new information into a text file


#reset the files so they have no data
with open(filename, 'w') as file:
    pass
with open(filename2, 'w') as file:
    pass

#get the first initial scan that will be compared against in future scans
if(Obj.Connect()):
        gen = Obj.StartScanning() #start scan
        
        pos=(next(gen)) #collect the first 360 values
            
            #put all 360 values into the LIDARdata.txt
        for p in range(360):
            with open(filename, 'a') as f:                
                f.write(f'{str(pos[p])} \t ')
            
        #end the scan
        Obj.StopScanning()
        Obj.Disconnect()
else:
    print("Error connecting to device")


#collect ten scans to put in the new data file 
def read_values():
    if(Obj.Connect()):
        gen = Obj.StartScanning() #start scan

        #scan ten times
        i=0
        while i <10:
            pos=(next(gen))
            
            #put all 360 values of each scan into the newlidardata.txt
            for p in range(360):
                with open(filename2, 'a') as f:                
                    f.write(f'{str(pos[p])} \t ')
            i=i+1
            
        
        Obj.StopScanning()
        Obj.Disconnect()
    else:
        print("Error connecting to device")


#compare the values of the initial scan in LIDARdata.txt to the latest scan in NewLidardata.txt
def compare_values():
    
    #put the values of LIDARdata.txt into lst1
    with open (filename, 'r') as file:
        content=file.read()
        lst1=content.split()
        lst1 = [int(item) for item in lst1]

    #put the last 360 values of NewLidardata.txt into lst2
    with open (filename2, 'r') as file:
        content=file.read()
        ten_vals=content.split()
        lst2=ten_vals[-360:]
        lst2=[int(value) for value in lst2]
    
    #determine the difference between lst1 and lst2
    diff_val=0
    for i in range(len(lst1)):
        diff_val+=(lst1[i]-lst2[i])^2

    #if the difference value is greater than 10 then a person is detected
    if diff_val>10:
        print("Person Detected")
    else:
        print("No Person Detected")
    return [lst1, lst2] #return the lists so they can be printed and observed




def init_polar_plot():
    angles = np.linspace(0, 2 * np.pi, 360, endpoint=False)
    plt.ion()
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    
    initial_data = np.zeros_like(angles)
    line1, = ax.plot(angles, initial_data, label='Initial Scan (lst1)')
    line2, = ax.plot(angles, initial_data, label='Latest Scan (lst2)', linestyle='--')
    
    ax.set_title("Live Polar Plot of LIDAR Data")
    ax.legend()
    return fig, ax, line1, line2, angles

def update_polar_plot(fig, ax, line1, line2, lst1, lst2, angles):
    if len(lst1) != len(angles) or len(lst2) != len(angles):
        print("Warning: Length mismatch between data and angles")
        return
    
    line1.set_ydata(lst1)
    line2.set_ydata(lst2)
    
    ax.set_ylim(0, max(max(lst1, default=0), max(lst2, default=0)))  # Adjust y-axis to fit data
    fig.canvas.draw()
    fig.canvas.flush_events()

# Initialize the plot
fig, ax, line1, line2, angles = init_polar_plot()




# in future make this infinite while loop that can he broken with the press of a button or key on keyboard 
a = 0
while a < 2:
    read_values()
    lst1, lst2 = compare_values()

    # print list contents
    print(lst1)
    print(lst2)

    # Update the plot with the latest data
    update_polar_plot(fig, ax, line1, line2, lst1, lst2, angles)

    # Reset the NewLidardata.txt for the next iteration
    with open(filename2, 'w') as file:
        pass

    a += 1

plt.ioff()
plt.show()



