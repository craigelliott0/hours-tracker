from tkinter import *
from tkinter import ttk
import pandas
import datetime


# ----- Dataframe ------
# Columns for:
# Date;
# Start/stop times;
# Total time between last start and stop;
# Action (ie. start, stop or reset of the timer)
# Session; a numerical value starting at 0; will increase +1 with each click of the reset button;
# breaks day tracking into separate sessions, enabling timer to be reset without deleting previous day data

logged_hours_df = pandas.read_csv("data.csv")
data_dict = pandas.DataFrame.to_dict(logged_hours_df)
day_dict = data_dict['Date']
start_time_dict = data_dict['Start/Stop']
total = data_dict['Total']
action = data_dict['Action']
session = data_dict['Session']

timer_reset = False
day_mode = True
# project_mode = False

# ----- Function to calculate total time worked for current day ----- #


def day_calc():
    current_df = pandas.read_csv("data.csv")
    today = datetime.datetime.today().strftime('%m/%d/%y')
    current_session = session[len(start_time_dict) -1]
    todays_sessions = current_df[current_df.Date == today]
    latest_sessions = todays_sessions[todays_sessions['Session'] == current_session]
    session_duration_list = latest_sessions['Total'].to_list()
    hours = []
    minutes = []
    seconds = []
    # The following for-loop iterates through the 'Total' column of the df.
    # Some values are empty (evaluate as NaN), hence the if-statement.
    for num in session_duration_list:
        if type(num) == str:
            new_num = num.split(':')
            # new_num is a list containing 3 strings (h, m, s)
            hours.append(int(new_num[0]))
            minutes.append(int(new_num[1]))
            seconds.append(int(new_num[2]))
    total_hours = sum(hours)
    total_min = sum(minutes)
    total_sec = sum(seconds)  # Will total more than 60
    print(f"total hours: {total_hours}, total mins: {total_min}, total sec: {total_sec}")
    # seconds into minutes calc
    remainder_sec = total_sec % 60  # Calculates leftover seconds that won't be converted into minutes. This figure will be displayed in the app as seconds
    total_sec -= remainder_sec  # Removes remainder from seconds list. The figure in the list will now divide evenly into minutes.
    sec_to_min = total_sec / 60  # Converts seconds into minutes
    total_min += sec_to_min  # And updates minutes list
    # minutes into hours calc
    remainder_min = total_min % 60
    total_min -= remainder_min
    min_to_hour = total_min / 60
    total_hours += min_to_hour
    canvas.itemconfig(day_total_display, text=f"{int(total_hours)}h {int(remainder_min)}m {remainder_sec}s")


timer_on = False
on_time = ''
off_time = ''


# --------- Function to start and stop timer ------------#

def start_stop():
    time = datetime.datetime.now().replace(microsecond=0)
    current_date = time.strftime("%x")
    current_time = time.strftime("%X")
    last_logged_date = day_dict[len(day_dict) -1]
    if current_date != last_logged_date:
        session[len(start_time_dict)] = 0
    else:
        session[len(start_time_dict)] = session[len(start_time_dict) - 1]
    global timer_on, on_time, off_time
    if not timer_on:
        timer_on = True
        on_time = time
        canvas.itemconfig(time_display, text=on_time.time())
        canvas.itemconfig(status_display, text="Working since...")
        if timer_reset:
            action[len(start_time_dict)] = 'Reset'
            session[len(start_time_dict)] += 1
        else:
            action[len(start_time_dict)] = 'Start'
    else:
        timer_on = False
        off_time = time
        canvas.itemconfig(time_display, text=off_time.time())
        canvas.itemconfig(status_display, text="Stopped at...")
        time_elapsed = off_time - on_time
        total[len(start_time_dict)] = time_elapsed
        action[len(start_time_dict)] = 'Stop'
    day_dict[len(start_time_dict)] = current_date
    start_time_dict[len(start_time_dict)] = current_time
    new_df = pandas.DataFrame.from_dict(data_dict)
    new_df.to_csv("data.csv", index=False)
    day_calc()


# ----- Reset Timer ------ #

def reset():
    if not timer_on:
        global timer_reset
        timer_reset = True
        canvas.itemconfig(day_total_display, text='0h 0m 0s')


# ----- Set Mode ----------#
def mode(select):
    global day_mode
    print(select)
    if select == "day":
        day_mode = True
        # project_mode = False
        print(f"Day mode is on")
    else:
        # project_mode = True
        day_mode = False
        print(f"Project mode is on")


# --------UI-----------

window = Tk()
window.title("Hours Tracker")
window.config(padx=10, pady=10, bg="white")

# notebook = ttk.Notebook(window)
# notebook.grid(column=0, row=0, pady=15)

# frame1 = Frame(notebook)
# frame2 = Frame(notebook)
#
# frame1.grid(column=0, row=0)
# frame2.grid(column=0, row=0)
#
# notebook.add(frame1, text='Timer')
# notebook.add(frame2, text='History')

bg_image = PhotoImage(file="hours_tracker_img.png")

canvas = Canvas(width=800, height=533)
canvas.create_image(400, 263, image=bg_image)

time_display = canvas.create_text(400, 145, text='00:00:00', font=("Ariel", 30, "bold"), fill='white')
status_display = canvas.create_text(300, 100, text='', font=("Ariel", 20, "italic"), fill='white')
day_total_text = canvas.create_text(580, 290, text="Today's total", font=("Ariel", 20, "italic"), fill='white')
mode_text = canvas.create_text(668, 505, text="Mode:", font=("Ariel", 15, "italic"), fill='black')
day_total_display = canvas.create_text(600, 320, text='0h 0m 0s', font=("Ariel", 20, "bold"), fill='white')

canvas.grid(column=0, row=0, columnspan=2)


start_btn = Button(text="START/STOP", font=("Ariel", 30, "bold"), highlightthickness=0, command=start_stop)
start_btn.grid(column=0, row=0)

reset_btn = Button(text='⟳', font=("Ariel", 10, "bold"), highlightthickness=0, command=reset)
reset_btn.place(x=300, y=300)

variable = StringVar(window)
variable.set("day")

mode_select = OptionMenu(window, variable, "day", "project", command=mode)
mode_select.place(x=700, y=495)

# if not day_mode:
#     print("test")
#     test_text = canvas.create_text(600, 495, text="Test:", font=("Ariel", 15, "italic"), fill='black')
#
#     var = StringVar(window)
#     var.set("--")
#
#     project_select = OptionMenu(window, var, "proj1", "proj2")
#     project_select.place(x=600, y=495)


window.mainloop()
