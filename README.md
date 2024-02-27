# hours-tracker

An app for tracking hours worked within a day. 

- The app is written in Python, and uses Pandas for a dataframe. It uses tkinter for a GUI. Run the code in your code editor to launch the GUI and interact with the app. 
- The app uses a date-time module and registers the time of each click of the start/stop button. 
- Each click is logged to a local csv file with the time and the relevant 'action': 'start' or 'stop' (or 'reset' in the event that the reset button is clicked).
- The difference between 'start' and 'stop' clicks is calculated and the total time for which the timer has been 'on' is displayed within the GUI as the total time worked so far within the current day.
- As the name suggests, the reset button will reset the total time worked within the current day to zero.
- Close the GUI to stop the program. As the data is saved to the csv, you may close the GUI in between uses of the app and it will continue to display the total time that has accrued for the day when the app is relaunched.
