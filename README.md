# Demcom Festival Schedulation

![example_01](img/overview_example_01.png)


## 

As a Houdini artist ( and soon to be Synthetic Data Engineer at Demcon! ), I couldn't resist doing this challenge in Houdini.

As far as using Python; I used Python (inside Houdini) to make main festival scheduler.

I added a copy of the code in "scripts/scheduler.py" that is used inside Houdini. I commented out some of the Houdini related code, so it should be able to run from a commandline.

The output is pushed downstream to proceduraly create a festival overview in Houdini.

All 1100+ Demcon employees are attending this festival. Make sure you plan ahead, because you have little time to go from one to the next, as you can see in the preview ;)

[![preview_festival](img/play_preview2.png)]( https://drive.google.com/file/d/1wzf1vK6FQn2MKWZ9W07eOYgYbjpq0Thf/view?usp=sharing )


## Comments


Created using Houdini 20.5.332 Py 3.11

Python code can be found in "scripts/scheduler.py" that is used in the Python node inside Houdini.  

It should be able to run standalone.



## Setup overview:


Everything is procedural generated, based on the amount of stages, start and end time.

Some key points:

![python node](img/hou_step_01_gen_schedule.png)
Here in the Python SOP node it generates the schedule based on the input .csv.
It generates a X amount of points based on the amount of shows found in the .csv file. Everything is put into array's and promoted to attributes to be used down stream.




