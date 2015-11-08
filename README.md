Classroom Scheduler (new/better name TBD)

When completed, this tool will manifest as a single page web app where you input a time, room, building, and day of the week, and you will get back whether or not there is a class on campus at that time. I use ScheduleParser.py to iterate through all classes in the UC Berkeley schedule of classes, and then iterate through each instance to create an entry in my sqlite3 database, pulling all data from the online API. Then, from the user's perspective when they enter in the pertinent information, I will make an http get request to a Flask application which will open the database and see if a class already occupies that spot, and then return yes/no. 

Current Issues:
Some sort of issue when parsing classes, Flask app not working, Webpage javascript to be written.
