This program is the foundation for a transportation manager program. It contains a web app that allows for a "dispatcher" to do a multitude of task.

# HOME PAGE:
From here you can view all current drivers that are working based on time(this displays in realtime).


# NEW DRIVER:

Here you can view a list of all drivers in the system and create a new one. Features include: Full Name, address, truck number,
shift start and end and the delivery zone they will work in(see notes).

# NEW ORDER:

Here you can create a new "order" for a driver to deliver. You can choose whether or not to auto select a driver(see notes) or choose one manually

# SHOW ROUTES FOR DRIVERS:

This page allows you to search past days and view a driver's workday and their total number of stops they did.

# MANAGE DAILY ROUTES:

Here you can see a list of all current jobs for the current workday(realtime) and modify them to switch drivers, delete the job or get 
directions for the specified order.

# NOTES:

- Delivery Zone - Part of my effort to make efficiency key was to create five "zones" of zip codes around the metro area: North, East, West, South and Central.
The idea is to keep drivers in their respective zones as much as possible to maximize their job effiency an prevent drivers from spending time and fuel driving
all over the city. The Concept is I don't care where they pick up the job but the delivery must be in the drivers zone to get the job.

- Auto Select - Here is where the meat of the program is, when you select this job the program will collect the destination zip code and 
find the appropriate driver to assign that job to. The program will take into account number of possible zones(as zones do overlap each other), 
if no zone is found the program will find the nearests zone to the destination, possible number of available drivers, workload of each driver and 
time of day to figure out who should get the job. If the dispathcer is unhappy with the program's selection they can update the driver in the 
"Manage Daily Routes" tab.
  
