# node = hou.pwd()
# geo = node.geometry()

# get .csv file path from parameter upstream
# csv_path = hou.pwd().parm("path").eval()
# use this outside Houdini:

# csv_path = "E:/HOUDINI/LABS/SCRIPTS/festival_schedule_generator/data_sheet.csv"

# use this to import lists directly from csvfile:
# order : show_name, start_time, end_time
import csv

csv_path = "data/data_sheet.csv"

with open(csv_path, newline='') as csvfile:
    showreader = csv.reader(csvfile)
    list_reader = [list(i) for i in showreader]

start_time = []
end_time = []
show_name = []

# create points for each entry and fill lists with show info
for sn, s, e in list_reader:
    # pt0 = geo.createPoint() # create point for every show
    start = start_time.append(int(s))
    end = end_time.append(int(e))
    shown = show_name.append(sn)
       
# show list from .csv:
show_list = [(start_time[i], end_time[i], show_name[i]) for i in range(0, len(show_name))]


class Stage:
    def __init__(self, stage_number):
        """
        Each stage represents a venue where shows can be scheduled.
        Args:
            stage_number (int): The unique identifier for the stage.
        """
        self.stage_number = stage_number # store stage number
        self.occupied_until = 0 # time until the stage is free
        self.shows = [] # Create an empty list to store scheduled shows

    def can_add_show(self, start_time):
        # Check if the new show's start time is after the stage's current occupation
        return start_time > self.occupied_until

    def add_show(self, show_name, start_time, end_time):
        """
        Adds a new show to the stage.
        """
        self.occupied_until = end_time # Update the stage's occupation time
        self.shows.append((start_time, end_time, show_name)) # Add the show to the stage's schedule

    def __lt__(self, other):
        """
        for use in stages.sort() so that stages that become free sooner are 
        prioritized when assigning new shows.
        """
        return self.occupied_until < other.occupied_until # Compare stages based on their free time


def schedule_bands(timetable):
    """
    schedules shows across different stages based on their start and end times.
    timetable (list): A list of tuples containing (start_time, end_time, show_name).
    """
    stages = [] # list to store stages
    show_schedule = {} # Create an empty dictionary to store the show-stage mapping
    timetable.sort()  # Sort the timetable by start time
    
    # Lists to store the final results to use in Houdini.
    show_names = []
    stage_numbers = []
    start_times = []
    end_times = []

    for start_time, end_time, show_name in timetable:
        assigned_stage = None # Initialize the assigned stage to None

        # Iterate through existing stages to find a suitable one
        for stage in stages:
            if stage.can_add_show(start_time): # Check if the stage is available
                stage.add_show(show_name, start_time, end_time) # Add the show to the stage
                show_schedule[show_name] = stage # Update the show-stage mapping
                assigned_stage = stage # Set the assigned stage
                stages.sort()  # Sort stages by occupied_until
                break # Break the loop if a suitable stage is found
        
        # If no suitable stage is found, create a new stage
        if assigned_stage is None:
            stage_number = len(stages) + 1 # Determine the new stage number
            new_stage = Stage(stage_number) # Create a new stage
            new_stage.add_show(show_name, start_time, end_time) # Add the show to the new stage
            show_schedule[show_name] = new_stage # Update the show-stage mapping
            stages.append(new_stage) # Add the new stage to the list
            stages.sort()  # Sort stages by occupied_until
            assigned_stage = new_stage # Set the assigned stage

        # append to lists
        show_names.append(show_name)
        stage_numbers.append(assigned_stage.stage_number)
        start_times.append(start_time)
        end_times.append(end_time)

    total_stages = len(stages) # total number of stages used
    return show_names, stage_numbers, start_times, end_times, total_stages


show_names, stage_numbers, start_times, end_times, total_stages = schedule_bands(show_list)

show_listss = [(stage_numbers[i], show_names[i], start_times[i], end_times[i]) for i in range(0, len(show_names))]
for i in show_listss:
    print("show_schedule:", i)

# # Create detail array attributes for each schedule info:
# geo.addArrayAttrib(hou.attribType.Global, "start_time_scheduling", hou.attribData.Int, tuple_size=1)
# geo.setGlobalAttribValue("start_time_scheduling", start_times)

# geo.addArrayAttrib(hou.attribType.Global, "end_time_scheduling", hou.attribData.Int, tuple_size=1)
# geo.setGlobalAttribValue("end_time_scheduling", end_times)    

# geo.addArrayAttrib(hou.attribType.Global, "stagename_scheduling", hou.attribData.String, tuple_size=1)
# geo.setGlobalAttribValue("stagename_scheduling", show_names)  


# # Create detail array attributes for stage number:
# geo.addArrayAttrib(hou.attribType.Global, "stage_index", hou.attribData.Int, tuple_size=1)
# geo.setGlobalAttribValue("stage_index", stage_numbers)  
# # Total stages attribute:    
# geo.addAttrib(hou.attribType.Global, "stage_numbers", total_stages)