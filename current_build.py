from tkinter import *
from PIL import ImageTk, Image
import pyodbc
import pandas as pd
from pandasgui import show
import time
import numpy as np

#---AZURE SQL CONNECTION--------------------------------------------------------
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=tcp:nbaserver.database.windows.net,1433;'
                      'Database=NBA;'
                      'Uid=huffbrim;'
                      'Pwd=Grauisgood1;'
                      'Encrypt=yes;'
                      'TrustServerCertificate=no;'
                      'Timeout=30;')
cursor = conn.cursor()
#-------------------------------------------------------------------------------
users = []
passes = []
actualuser = []
player_hints = []
descriptions = []
loginwin = Tk()
loginwin.title("Provide Login Credentials")
loginwin.configure(bg='gray10')
loginwin.geometry("475x275+600+300")
#----LOGIN WINDOW FUNCTIONS-----------------------------------------------------
def send_credentials(usr, pas):
    global userglobal
    userglobal = usr

    ind = 0
    userpassq = pd.read_sql_query("SELECT * FROM user_data", conn)
    count = len(userpassq.index)
    i = 0
    while True:
        users.append(userpassq['Username'].values[i].strip())
        i += 1
        if i >= count:
            break
    j = 0
    while True:
        passes.append(userpassq['drowssap'].values[j].strip())
        j += 1
        if j >= count:
            break

    for ele in users:
        if ele == usr:
            ind = users.index(usr)
            if passes[ind] == pas:
                actualuser.append(ele)

                loginwin.destroy()

    users.clear()
    passes.clear()
def exiter():
    exit()
def create_new(usr, pas):
    global user
    user = (usr + "_rosters")

    cursor.execute("INSERT INTO user_data (Username, drowssap, [ip address]) VALUES ('"+usr+"', '"+pas+"', '')")
    cursor.execute("CREATE TABLE " +user+ " (roster_name nchar(15), [Player Name] varchar(50), [Player_Hint] varchar(MAX), [description] varchar(MAX));")
    conn.commit()
    #----GUI FOR SUCCESS MESSAGE-----
    anewwindow = Toplevel()
    anewwindow.title("")
    anewwindow.configure(bg='gray86')
    anewwindow.geometry("300x150+600+300")
                                                                              #---
    announce = Label(anewwindow, text="Congrats, please exit the application\n and rerun under new credentials", padx=50, pady=5, bg='gray86')                               #---
    announce.config(font=("fixedsys", 8))
    announce.pack()
    b = Button(anewwindow, text="EXIT",command=exiter, padx=50, pady=5, bg='Salmon')
    b.config(font=("fixedsys", 12))
    b.pack()
#----GUI FOR LOGIN--------------------------------------------------------------
log = Label(loginwin, text="LOGIN: ", pady=10, bg='gray10', fg='white smoke')
log.config(font=("fixedsys", 12))
log.grid(row=0, column=0,columnspan=3)

usrnm = Label(loginwin, text="USERNAME: ", pady=10, bg='gray10', fg='white smoke')
usrnm.config(font=("fixedsys", 12))
usrnm.grid(row=1, column=0, sticky = 'e')
u = Entry(loginwin, width=30, borderwidth=2, bg='gray50')
u.config(font=("fixedsys", 12))
u.grid(row=1, column=1,columnspan=2, padx=10, pady=10)

asswrd = Label(loginwin, text="PASSWORD: ", pady=10, bg='gray10', fg='white smoke')
asswrd.config(font=("fixedsys", 12))
asswrd.grid(row=2, column=0, sticky = 'e')
p = Entry(loginwin,show="*", width=30, borderwidth=2, bg='gray50')
p.config(font=("fixedsys", 12))
p.grid(row=2, column=1,columnspan=2, padx=10, pady=10)

submit = Button(loginwin, text="SUBMIT",command=lambda:send_credentials(u.get(), p.get()), pady=10, bg='gray25', fg='white smoke')
submit.config(font=("fixedsys", 12))
submit.grid(row=1, column=3,rowspan=2, sticky = 'nswe')

cnew = Label(loginwin, text="OR CREATE NEW ACCOUNT: ", pady=10, bg='gray10', fg='white smoke')
cnew.config(font=("fixedsys", 12))
cnew.grid(row=4, column=0,columnspan=3)

usrnm2 = Label(loginwin, text="USERNAME: ", pady=10, bg='gray10', fg='white smoke')
usrnm2.config(font=("fixedsys", 12))
usrnm2.grid(row=5, column=0, sticky = 'e')
l = Entry(loginwin, width=30, borderwidth=2, bg='gray50')
l.config(font=("fixedsys", 12))
l.grid(row=5, column=1,columnspan=2, padx=10, pady=10)

asswrd2 = Label(loginwin, text="PASSWORD: ", pady=10, bg='gray10', fg='white smoke')
asswrd2.config(font=("fixedsys", 12))
asswrd2.grid(row=6, column=0, sticky = 'e')
m = Entry(loginwin,show="*", width=30, borderwidth=2, bg='gray50')
m.config(font=("fixedsys", 12))
m.grid(row=6, column=1,columnspan=2, padx=10, pady=10)

submit2 = Button(loginwin, text="CREATE", command=lambda:create_new(l.get(), m.get()) ,pady=10, bg='white smoke')
submit2.config(font=("fixedsys", 12), width=10)
submit2.grid(row=5, column=3,rowspan=2, sticky = 'nswe')
loginwin.mainloop()

#---DEFINING GUI----------------------------------------------------------------
if len(actualuser) >= 1:
    usrtitle = ("Welcome back " + actualuser[0])
else:
    usrtitle = 'GUEST'
root = Tk()
root.title(usrtitle)
root.geometry("1210x590")
root.configure(bg='gray86')
#root.overrideredirect(True)
#root.iconbitmap('C:/Users/iabri/Desktop/atom_files_scripts/bball.ico')
#-----MENU BARS & MENU BAR FUNCTIONS--------------------------------------------
#-------------------------------------------------------------------------------
#----GLOBALS--------------------------------------------------------------------
searchable_list = ["Player Name","Team","Position","Age", "Roster"]
all_categories = ['SELECT ALL','Age','Team','Games Played','Games Started','Minutes Played Per Game',
                'Field Goals Per Game','Field Goal Attmpts Per Game','Field Goal Percentage',
                '3-Point Field Goals Per Game','3-Point Field Goal Attempts Per Game','3-Point Field Goal Percentage',
                '2-Point Field Goals Per Game','2-Point Field Goal Attempts Per Game','2-Point Field Goal Percentage',
                'Effective Field Goal Percentage','Free Throws Per Game','Free Throw Attempts Per Game',
                'Free Throw Percentage','Offensive Rebounds Per Game','Defensive Rebounds Per Game',
                'Total Rebounds Per Game','Assists Per Game','Steals Per Game','Blocks Per Game',
                'Turnovers Per Game','Personal Fouls Per Game','Points Per Game']
user_selected_categories =[]
rosters = ["MY QUIZZES"]
indexable_rosters = []
team_affil = []
user_tables = []
#-----FUNCTIONS-----------------------------------------------------------------
#  _______________ __________  ____________________.___________    _______    _________
#  \_   _____/    |   \      \ \_   ___ \__    ___/|   \_____  \   \      \  /   _____/
#   |    __) |    |   /   |   \/    \  \/ |    |   |   |/   |   \  /   |   \ \_____  \
#   |     \  |    |  /    |    \     \____|    |   |   /    |    \/    |    \/        \
#   \___  /  |______/\____|__  /\______  /|____|   |___\_______  /\____|__  /_______  /
#       \/                   \/        \/                      \/         \/        \/
def adv_querysearch():
    ans1 = formatList(user_selected_categories)
    if clicked.get() == "Player Name":
        user_selected_categories.insert(0, "Player Name")
        ans1 = formatList(user_selected_categories)
        if "SELECT ALL" in user_selected_categories:
            ans1 = "*"
    if clicked.get() == "Age":
        user_selected_categories.insert(0, "Age")
        user_selected_categories.insert(0, "Player Name")
        ans1 = formatList(user_selected_categories)
        if "SELECT ALL" in user_selected_categories:
            ans1 = "*"
    if clicked.get() == "Team":
        user_selected_categories.insert(0, "Team")
        user_selected_categories.insert(0, "Player Name")
        ans1 = formatList(user_selected_categories)
        if "SELECT ALL" in user_selected_categories:
            ans1 = "*"
    if clicked.get() == "Position":
        user_selected_categories.insert(0, "Position")
        user_selected_categories.insert(0, "Player Name")
        ans1 = formatList(user_selected_categories)
        if "SELECT ALL" in user_selected_categories:
            ans1 = "*"
    if clicked.get() == "Roster":
        user_selected_categories.insert(0, "Player Name")
        ans1 = formatList(user_selected_categories)
        if "SELECT ALL" in user_selected_categories:
            ans1 = "*"

        i = 0
        for rows in indexable_rosters:
            if q.get() in  indexable_rosters[i]:
                global truncated_rost
                truncated_rost = indexable_rosters[i][1:]
            i += 1
            if i >= len(indexable_rosters):
                break
        formatted_players = roster_query(truncated_rost)
        query = pd.read_sql_query("SELECT "+ ans1 +" FROM per_game_stats WHERE [Player Name] LIKE '"+ formatted_players +"'",conn)
        show(query)
    else:
        ans2="["+clicked.get()+"]"
        query = pd.read_sql_query("SELECT "+ ans1 +" FROM per_game_stats WHERE "+ ans2 +" LIKE '%"+ q.get() +"%'",conn)
        show(query)
#-------------------------------------------------------------------------------
def roster_query(players_list):
    format = another_format=(players_list)
    joint = "' OR [Player Name] LIKE '".join(format)
    return joint
#-------------------------------------------------------------------------------
def another_format(list):
    str1 = ""
    str2 = "'"
    str3 = "'"
    for ele in list:
        str1 += (str3 + ele + str2)
    str1 = str1
    return str1
#--SELECTS CORRECT TEAM AFFLIATION FOR PLAYER-----------------------------------
def add_to_team(var):
    pass
#---CREATES NEW ROSTER AND OVERWRITES MY QUIZZES DROPDOWN-----------------------
def new_roster():

    #make a new window to write a short quiz description -----------------------
    desc_window = Toplevel()
    desc_window.title("DESCRIPTION")
    desc_window.configure(bg='gray86')

    quiz_desc = Label(desc_window, text="Write a descriptino: ", pady=10, bg='gray86')
    quiz_desc.config(font=("fixedsys", 12))
    quiz_desc.grid(row=0, column=0, rowspan=2, sticky='w')

    global desc
    desc = Entry(desc_window, width=30, borderwidth=2, bg='gray50', fg='white smoke')
    desc.config(font=("fixedsys", 12))
    desc.grid(row=0, column=1,rowspan=2, sticky='w')

    apply_desc = Button(desc_window, text="SUBMIT",command=lambda:[add_description(n.get(), desc.get())], bg='light slate gray', bd=2, fg='gray90')
    apply_desc.config(font=("fixedsys", 12), width=25)
    apply_desc.grid(row=0, column=2,rowspan=2, sticky='w')
#-----
    if n.get() not in rosters:
        rosters.append(n.get())
        if "MY QUIZZES" in rosters:
            rosters.remove("MY QUIZZES")
    if n.get() not in indexable_rosters:
        indexable_rosters.append([n.get()])

    global clicker
    clicker = StringVar()
    clicker.set(rosters[0])
    my_rosters = OptionMenu(root, clicker, *rosters)
    my_rosters.grid(sticky='nswe')
    my_rosters["menu"].config(font=("fixedsys", 8), bg="gray86")
    my_rosters.config(width = 11, font=("fixedsys", 12),  bg='gray86',  bd=1, highlightbackground="light slate gray", highlightcolor="light slate gray", highlightthickness=2,relief='groove')
    my_rosters.grid(row=6, column=3,columnspan=2, sticky='nswe', pady=5)

    viewhbtn = Button(root,text="VIEW", command=lambda:view_roster(), bg='light slate gray', bd=2, fg='gray90')
    viewhbtn.config(font=("fixedsys", 12))
    viewhbtn.grid(row=5, column=5, sticky='nswe', pady=5, padx=10)
#--RUNS ALL STATS ON ENTIRE ROSTER----------------------------------------------
def roster_report():
    ####-----THIS IS SUPER ENNEFICIENT AND NEEDS FIXED IN THE FUTURE______!!!!!
    selectall1 = "SELECT * FROM per_game_stats WHERE [Player Name] LIKE '%"
    #1 PLAYERs
    if len(the_rost) ==1:
        roster = pd.read_sql_query(selectall1+str(the_rost[0])+"%'", conn)
        show(roster)
    #2 PLAYERs
    if len(the_rost) ==2:
        roster = pd.read_sql_query(selectall1+str(the_rost[0])+"%'"+" OR [Player Name] LIKE '%"+str(the_rost[1])+"%'", conn)
        show(roster)
    #3 PLAYERs
    if len(the_rost) ==3:
        roster = pd.read_sql_query(selectall1+str(the_rost[0])+"%'"+" OR [Player Name] LIKE '%"+str(the_rost[1])+"%'"+
        " OR [Player Name] LIKE '%"+str(the_rost[2])+"%'", conn)
        show(roster)
    #4 PLAYERs
    if len(the_rost) ==4:
        roster = pd.read_sql_query(selectall1+str(the_rost[0])+"%'"+" OR [Player Name] LIKE '%"+str(the_rost[1])+"%'"+
        " OR [Player Name] LIKE '%"+str(the_rost[2])+"%'"+" OR [Player Name] LIKE '%"+str(the_rost[3])+"%'", conn)
        show(roster)
    #5 PLAYERs
    if len(the_rost) ==5:
        roster = pd.read_sql_query(selectall1+str(the_rost[0])+"%'"+" OR [Player Name] LIKE '%"+str(the_rost[1])+"%'"+
        " OR [Player Name] LIKE '%"+str(the_rost[2])+"%'"+" OR [Player Name] LIKE '%"+str(the_rost[3])+"%'"+
        " OR [Player Name] LIKE '%"+str(the_rost[4])+"%'", conn)
        show(roster)
    #6 PLAYERs
    if len(the_rost) ==6:
        roster = pd.read_sql_query(selectall1+str(the_rost[0])+"%'"+" OR [Player Name] LIKE '%"+str(the_rost[1])+"%'"+
        " OR [Player Name] LIKE '%"+str(the_rost[2])+"%'"+" OR [Player Name] LIKE '%"+str(the_rost[3])+"%'"+
        " OR [Player Name] LIKE '%"+str(the_rost[4])+"%'"+" OR [Player Name] LIKE '%"+str(the_rost[5])+"%'", conn)
        show(roster)
    #7 PLAYERs
    if len(the_rost) ==7:
        roster = pd.read_sql_query(selectall1+str(the_rost[0])+"%'"+" OR [Player Name] LIKE '%"+str(the_rost[1])+"%'"+
        " OR [Player Name] LIKE '%"+str(the_rost[2])+"%'"+" OR [Player Name] LIKE '%"+str(the_rost[3])+"%'"+
        " OR [Player Name] LIKE '%"+str(the_rost[4])+"%'"+" OR [Player Name] LIKE '%"+str(the_rost[5])+"%'"+
        " OR [Player Name] LIKE '%"+str(the_rost[6])+"%'", conn)
        show(roster)
    #8 PLAYERs
    if len(the_rost) ==8:
        roster = pd.read_sql_query(selectall1+str(the_rost[0])+"%'"+" OR [Player Name] LIKE '%"+str(the_rost[1])+"%'"+
        " OR [Player Name] LIKE '%"+str(the_rost[2])+"%'"+" OR [Player Name] LIKE '%"+str(the_rost[3])+"%'"+
        " OR [Player Name] LIKE '%"+str(the_rost[4])+"%'"+" OR [Player Name] LIKE '%"+str(the_rost[5])+"%'"+
        " OR [Player Name] LIKE '%"+str(the_rost[6])+"%'"+" OR [Player Name] LIKE '%"+str(the_rost[7])+"%'", conn)
        show(roster)
    #9 PLAYERs
    if len(the_rost) ==9:
        roster = pd.read_sql_query(selectall1+str(the_rost[0])+"%'"+" OR [Player Name] LIKE '%"+str(the_rost[1])+"%'"+
        " OR [Player Name] LIKE '%"+str(the_rost[2])+"%'"+" OR [Player Name] LIKE '%"+str(the_rost[3])+"%'"+
        " OR [Player Name] LIKE '%"+str(the_rost[4])+"%'"+" OR [Player Name] LIKE '%"+str(the_rost[5])+"%'"+
        " OR [Player Name] LIKE '%"+str(the_rost[6])+"%'"+" OR [Player Name] LIKE '%"+str(the_rost[7])+"%'"+
        " OR [Player Name] LIKE '%"+str(the_rost[8])+"%'", conn)
        show(roster)
    #10 PLAYERs
    if len(the_rost) >=10:
        roster = pd.read_sql_query(selectall1+str(the_rost[0])+"%'"+" OR [Player Name] LIKE '%"+str(the_rost[1])+"%'"+
        " OR [Player Name] LIKE '%"+str(the_rost[2])+"%'"+" OR [Player Name] LIKE '%"+str(the_rost[3])+"%'"+
        " OR [Player Name] LIKE '%"+str(the_rost[4])+"%'"+" OR [Player Name] LIKE '%"+str(the_rost[5])+"%'"+
        " OR [Player Name] LIKE '%"+str(the_rost[6])+"%'"+" OR [Player Name] LIKE '%"+str(the_rost[7])+"%'"+
        " OR [Player Name] LIKE '%"+str(the_rost[8])+"%'"+" OR [Player Name] LIKE '%"+str(the_rost[9])+"%'", conn)
        show(roster)
#--ALLOWS THE USE OF QUERY BUILDER WITH YOUR PREMADE ROSTERS--------------------
def individual_roster_report():
    selectall1 = "SELECT * FROM per_game_stats WHERE [Player Name] LIKE '%"
    #1 PLAYERs
    if len(truncated_rost) ==1:
        roster = pd.read_sql_query(selectall1+str(truncated_rost[0])+"%'", conn)
        show(roster)
    #2 PLAYERs
    if len(truncated_rost) ==2:
        roster = pd.read_sql_query(selectall1+str(truncated_rost[0])+"%'"+" OR [Player Name] LIKE '%"+str(truncated_rost[1])+"%'", conn)
        show(roster)
    #3 PLAYERs
    if len(truncated_rost) ==3:
        roster = pd.read_sql_query(selectall1+str(truncated_rost[0])+"%'"+" OR [Player Name] LIKE '%"+str(truncated_rost[1])+"%'"+
        " OR [Player Name] LIKE '%"+str(truncated_rost[2])+"%'", conn)
        show(roster)
    #4 PLAYERs
    if len(truncated_rost) ==4:
        roster = pd.read_sql_query(selectall1+str(truncated_rost[0])+"%'"+" OR [Player Name] LIKE '%"+str(truncated_rost[1])+"%'"+
        " OR [Player Name] LIKE '%"+str(truncated_rost[2])+"%'"+" OR [Player Name] LIKE '%"+str(truncated_rost[3])+"%'", conn)
        show(roster)
    #5 PLAYERs
    if len(truncated_rost) ==5:
        roster = pd.read_sql_query(selectall1+str(truncated_rost[0])+"%'"+" OR [Player Name] LIKE '%"+str(truncated_rost[1])+"%'"+
        " OR [Player Name] LIKE '%"+str(truncated_rost[2])+"%'"+" OR [Player Name] LIKE '%"+str(truncated_rost[3])+"%'"+
        " OR [Player Name] LIKE '%"+str(truncated_rost[4])+"%'", conn)
        show(roster)
    #6 PLAYERs
    if len(truncated_rost) ==6:
        roster = pd.read_sql_query(selectall1+str(truncated_rost[0])+"%'"+" OR [Player Name] LIKE '%"+str(truncated_rost[1])+"%'"+
        " OR [Player Name] LIKE '%"+str(truncated_rost[2])+"%'"+" OR [Player Name] LIKE '%"+str(the_truncated_rostrost[3])+"%'"+
        " OR [Player Name] LIKE '%"+str(truncated_rost[4])+"%'"+" OR [Player Name] LIKE '%"+str(truncated_rost[5])+"%'", conn)
        show(roster)
    #7 PLAYERs
    if len(truncated_rost) ==7:
        roster = pd.read_sql_query(selectall1+str(truncated_rost[0])+"%'"+" OR [Player Name] LIKE '%"+str(truncated_rost[1])+"%'"+
        " OR [Player Name] LIKE '%"+str(truncated_rost[2])+"%'"+" OR [Player Name] LIKE '%"+str(truncated_rost[3])+"%'"+
        " OR [Player Name] LIKE '%"+str(truncated_rost[4])+"%'"+" OR [Player Name] LIKE '%"+str(truncated_rost[5])+"%'"+
        " OR [Player Name] LIKE '%"+str(truncated_rost[6])+"%'", conn)
        show(roster)
    #8 PLAYERs
    if len(truncated_rost) ==8:
        roster = pd.read_sql_query(selectall1+str(truncated_rost[0])+"%'"+" OR [Player Name] LIKE '%"+str(truncated_rost[1])+"%'"+
        " OR [Player Name] LIKE '%"+str(truncated_rost[2])+"%'"+" OR [Player Name] LIKE '%"+str(truncated_rost[3])+"%'"+
        " OR [Player Name] LIKE '%"+str(truncated_rost[4])+"%'"+" OR [Player Name] LIKE '%"+str(truncated_rost[5])+"%'"+
        " OR [Player Name] LIKE '%"+str(truncated_rost[6])+"%'"+" OR [Player Name] LIKE '%"+str(truncated_rost[7])+"%'", conn)
        show(roster)
    #9 PLAYERs
    if len(truncated_rost) ==9:
        roster = pd.read_sql_query(selectall1+str(truncated_rost[0])+"%'"+" OR [Player Name] LIKE '%"+str(truncated_rost[1])+"%'"+
        " OR [Player Name] LIKE '%"+str(truncated_rost[2])+"%'"+" OR [Player Name] LIKE '%"+str(truncated_rost[3])+"%'"+
        " OR [Player Name] LIKE '%"+str(truncated_rost[4])+"%'"+" OR [Player Name] LIKE '%"+str(truncated_rost[5])+"%'"+
        " OR [Player Name] LIKE '%"+str(truncated_rost[6])+"%'"+" OR [Player Name] LIKE '%"+str(truncated_rost[7])+"%'"+
        " OR [Player Name] LIKE '%"+str(truncated_rost[8])+"%'", conn)
        show(roster)
    #10 PLAYERs
    if len(truncated_rost) >=10:
        roster = pd.read_sql_query(selectall1+str(truncated_rost[0])+"%'"+" OR [Player Name] LIKE '%"+str(truncated_rost[1])+"%'"+
        " OR [Player Name] LIKE '%"+str(truncated_rost[2])+"%'"+" OR [Player Name] LIKE '%"+str(truncated_rost[3])+"%'"+
        " OR [Player Name] LIKE '%"+str(truncated_rost[4])+"%'"+" OR [Player Name] LIKE '%"+str(truncated_rost[5])+"%'"+
        " OR [Player Name] LIKE '%"+str(truncated_rost[6])+"%'"+" OR [Player Name] LIKE '%"+str(truncated_rost[7])+"%'"+
        " OR [Player Name] LIKE '%"+str(truncated_rost[8])+"%'"+" OR [Player Name] LIKE '%"+str(truncated_rost[9])+"%'", conn)
        show(roster)
#--SELECT FROM DROPDOWN WHICH ROSTER TO VIEW------------------------------------
def view_roster():

    i = 0
    for rows in indexable_rosters:
        if clicker.get() in  indexable_rosters[i]:
            global truncated_rost
            truncated_rost = indexable_rosters[i][1:]

            roster_window = Toplevel()
            roster_window.title("")
            roster_window.configure(bg='gray86')
            decklbl = Label(roster_window, text=clicker.get(), padx=50, pady=5, bg='gray86')
            decklbl.config(font=("fixedsys", 14))
            decklbl.pack()

            j = 0
            while True:
                view_my_roster = Label(roster_window, text=truncated_rost[j], padx=5, pady=5, bg='gray86')
                view_my_roster.config(font=("fixedsys", 10))
                view_my_roster.pack()
                j += 1
                if j >= len(truncated_rost):
                    break

            analbtn = Button(roster_window, text="ANALYZE Quiz", command=individual_roster_report, bg='khaki')
            analbtn.config(font=("fixedsys", 12), width=25)
            analbtn.pack()
            backbtn = Button(roster_window, text="BACK", command=roster_window.destroy, bg='Salmon')
            backbtn.config(font=("fixedsys", 12), width=25)
            backbtn.pack()

        i += 1
        if i >= len(indexable_rosters):
            break
#---PULLS UP A FEW QUICK STATS OF SEARCHED PLAYER AND ALLOWS YOU TO ADD.......
#...SAID PLAYER TO YOUR DESIRED ROSTER------------------------------------------
def card_builder():
    global name
    query1 = pd.read_sql_query("SELECT [Player Name], Age, Team, [Position], [Points Per Game] FROM per_game_stats WHERE [Player Name] LIKE '%"+ e.get() +"%'", conn)
    name = query1['Player Name'].values[0]                                              #returns Name
    age = query1['Age'].values[0]                                                       #returns age
    team = query1['Team'].values[0]                                                     #returns team
    pos = query1['Position'].values[0]                                                  #returns position
    ppg = query1['Points Per Game'].values[0]

    global card_frame
    card_frame = LabelFrame(root, text=name, padx=5, pady=5, bg='gray86')
    card_frame.config(font=("fixedsys", 14))
    card_frame.grid(row=4, column=3, padx=20, pady=10, columnspan=2, sticky='nswe')

    global multiple
    if len(query1) >1 and query1['Player Name'].values[0] == query1['Player Name'].values[1] :                                                                                                                                                             #-
        multiple = LabelFrame(card_frame, text='SELECT TEAM AFFILIATION', padx=5, pady=5, bg='gray86', fg='light slate gray')
        multiple.config(font=("fixedsys", 12))
        multiple.grid(row=0, column=0)
        choose_player = pd.read_sql_query("SELECT [Player Name], [Team] FROM per_game_stats WHERE [Player Name] LIKE '%"+ name +"%'",conn)
        count = len(choose_player)
        i = 0
        c = ""
        z = ""
        while True:
            if i == 0:
                c = 'gray86'
                z = 'black'
            else:
                c = 'khaki'
                z = 'black'
            pteam = choose_player['Team'].values[i]
            teambtn = Button(multiple, text=pteam,command=lambda:add_to_team(pteam), padx=5, pady=5, bg=c, fg=z)
            teambtn.config(font=("fixedsys", 10))
            teambtn.grid(row=0, column=i)
            i += 1
            if i >= count:
                break

    global player_name

    global player_age
    player_age = Label(card_frame, text="Age: "+str(age), pady=10, bg='gray86')
    player_age.config(font=("fixedsys", 12))
    player_age.grid(row=1, column=0,sticky='w')

    global player_team
    player_team = Label(card_frame, text="Team: "+str(team), pady=10, bg='gray86')
    player_team.config(font=("fixedsys", 12))
    player_team.grid(row=2, column=0,sticky='w')

    global player_pos
    player_pos = Label(card_frame, text="Position: " +str(pos), pady=10, bg='gray86')
    player_pos.config(font=("fixedsys", 12))
    player_pos.grid(row=3, column=0,sticky='w')

    global player_ppg
    player_ppg = Label(card_frame, text="PPG: " +str(ppg), pady=10, bg='gray86')
    player_ppg.config(font=("fixedsys", 12))
    player_ppg.grid(row=4, column=0,sticky='w')

    if "MY QUIZZES" in rosters:
        rosters.remove("MY QUIZZES")
    global clickert
    clickert = StringVar()
    clickert.set("CHOOSE ROSTER")
    my_rosters2 = OptionMenu(card_frame, clickert, *rosters)                                                  #drop down for initial search parameters
    my_rosters2.grid(sticky='nswe')
    my_rosters2["menu"].config(font=("fixedsys", 8), bg="gray86")
    my_rosters2.config(width = 11, font=("fixedsys", 12),  bg='gray86',  bd=1, highlightbackground="light slate gray", highlightcolor="light slate gray", highlightthickness=2,relief='groove')                                                                         #----
    my_rosters2.grid(row=5, column=0, sticky='nswe', pady=5)

    add = Button(card_frame,text="ADD", command=lambda:[getridof(), hinter(), add_to_corrrect_roster(),add_to_deck()]  , bg='light slate gray', fg="gray90")
    add.config(font=("fixedsys", 12), width=20)
    add.grid(row=5, column=1,sticky='w', padx=15)


#--ADD aplayer hint to databse------------------------------------------------
def hinter():
    hintwindow = Toplevel()
    hintwindow.title("HINT")
    hintwindow.configure(bg='gray86')


    global quiz_hint
    player_hint = Label(hintwindow, text="Write a hint: ", pady=10, bg='gray86')
    player_hint.config(font=("fixedsys", 12))
    player_hint.grid(row=0, column=0,sticky='w')

    hint = Entry(hintwindow, width=30, borderwidth=2, bg='gray50')
    hint.config(font=("fixedsys", 12))
    hint.grid(row=0, column=1,sticky='w')
    print(userglobal)
    print(name)
    print(hint.get())
    apply_hint = Button(hintwindow, text="APPLY HINT",command=lambda:[addto_playerhints(name, hint.get())], bg='light slate gray', bd=2, fg='gray90')
    apply_hint.config(font=("fixedsys", 12), width=25)
    apply_hint.grid(row=0, column=2,sticky='w')
    global hintforsave
    hintforsave = hint.get().strip()
#-------------------------------------------------------------------------------
def addto_playerhints(name, hint):
    player_hints.append(name)
    player_hints.append(hint)
    print(player_hints)
def add_description(rosname, descrip):
    descriptions.append(rosname)
    descriptions.append(descrip)
    print(descriptions)
#--ADDS THE PLAYER HINT TO THE DB-----------------------------------------------
def hint_to_db(actualhint):
    global dahint
    dahint = actualhint.strip()
    print(dahint)

    cursor.execute(("UPDATE [dbo]."+userglobal+"_rosters SET [Player_Hint] = '"+dahint+"' WHERE [Player Name] LIKE '%"+name+"%';"))

#---ADDS PLAYER TO CORRECT ROSTER IN A 2-DIMENSIONAL LIST-----------------------
def add_to_corrrect_roster():
    i = 0
    for rows in indexable_rosters:
        if clickert.get() in  indexable_rosters[i]:
            if name not in indexable_rosters[i]:
                indexable_rosters[i].append(name)
        else:
            i += 1
#--REMOVES CARD-FRAME AFTER ADDING TO ROSTER------------------------------------
#--WILL NEED TO UTILIZE .CONFIG TO UPDATE INSTEAD OF DESTROY IN THE FUTURE------
def getridof():
    card_frame.destroy()
#--OPENS A SECOND WINDOW AFTER ADDING TO A ROSTER TO VIEW CHANGES MADE----------
def add_to_deck():
    newwindow = Toplevel()
    newwindow.title("")
    newwindow.configure(bg='gray86')
    decklbl = Label(newwindow, text=clickert.get(), padx=50, pady=5, bg='gray86')
    decklbl.config(font=("fixedsys", 14))
    decklbl.pack()

    global the_rost
    i = 0
    while True:
        if clickert.get() in indexable_rosters[i]:
            the_rost = indexable_rosters[i][1:]
        i += 1
        if i >= len(indexable_rosters):
            break

    if len(indexable_rosters) > 100:
        too_big = Label(newwindow, text="YOU HAVE REACHED MAX ROSTER SIZE", padx=5, pady=5, bg='gray86')
        too_big.config(font=("fixedsys", 10))
        too_big.pack()
        i = 0
        while True:
            plylbl = Label(newwindow, text=the_rost[i], padx=5, pady=5, bg='gray86')
            plylbl.config(font=("fixedsys", 10))
            plylbl.pack()
            i += 1
            if(i >= 10):
                break
    else:
        #LOOP to display entire roster------------------------------------------
        i = 0
        while True:
            plylbl = Label(newwindow, text=the_rost[i], padx=5, pady=5, bg='gray86')
            plylbl.config(font=("fixedsys", 10))
            plylbl.pack()
            i += 1
            if(i >= len(the_rost)):
                break
    backbtn = Button(newwindow, text="ANALYZE Quiz", command=roster_report, bg='khaki')
    backbtn.config(font=("fixedsys", 12), width=25)
    backbtn.pack()
    backbtn = Button(newwindow, text="BACK", command=newwindow.destroy, bg='Salmon')
    backbtn.config(font=("fixedsys", 12), width=25)
    backbtn.pack()
#--LOADS USERS QUERY BEFORE SEARCHING WITH DESIRED CRITERIA---------------------
def load_query():
    if clicked2.get() not in user_selected_categories:
        user_selected_categories.append(clicked2.get())
        #this is where we will pack our user query frame
        find_last = len(user_selected_categories)
        global outer
        if query_frame.winfo_exists() == 1:
            outer = Label(query_frame, text=user_selected_categories[find_last -1], anchor=W, bg='gray86')
            outer.config(font=("fixedsys", 12))
            outer.pack()
        else:
            outer = Label(query_frame2, text=user_selected_categories[find_last -1], anchor=W, bg='gray86')
            outer.config(font=("fixedsys", 12))
            outer.pack()
#--DELETES LAST ITEM ADDED TO QUERY, NEEDS UPDATED TO CONTINUE DELETION IN FUT--
def del_query():
    if len(user_selected_categories) > 0:
        outer.destroy()
        user_selected_categories.pop()
#--EMPTIES QUERY BUILDER FRAME--------------------------------------------------
def del_qframe():
    user_selected_categories.clear()
    query_frame.destroy()

    global query_frame2
    query_frame2 = LabelFrame(root, text="ADVANCED QUERY BUILDER", padx=5, pady=5, bg='gray86')
    query_frame2.grid(sticky='nswe')
    query_frame2.config(font=("fixedsys", 14))
    query_frame2.grid(row=4, column=0,rowspan=6,columnspan=2, padx=10, pady=10)
    q = Label(query_frame2, text="Current Query:", bg='gray86')
    q.config(font=("fixedsys", 12))
    q.pack()
#--SAVES ALL ROSTERS CREATED TO DATABASE FOR FUTURE USE / MANIPULATION----------
def sav_rosters():
    the_user = str(actualuser[0]) + "_rosters"
    alength = len(indexable_rosters)
    cursor.execute("truncate table "+the_user)#removes all data from table to prep reload
    k = 0
    j = 1
    #the while statement adds all your rosters & players accordingly to the server
    while True:
        cursor.execute("INSERT INTO "+the_user+" (roster_name, [Player Name]) VALUES ('"+indexable_rosters[k][0]+"', '"+indexable_rosters[k][j]+"')")
        j += 1
        if j >= len(indexable_rosters[k]):
            k += 1
            j = 1
        if k >= alength:
            break

    p = 0
    o = 1
    while True:
        cursor.execute(("UPDATE [dbo]."+userglobal+"_rosters SET [Player_Hint] = '"+player_hints[o]+"' WHERE [Player Name] LIKE '%"+player_hints[p]+"%';"))
        print(player_hints[o])
        print(player_hints[p])
        o += 2
        p += 2
        if p >= len(player_hints):
            break

    z = 0
    q = 1
    while True:
        cursor.execute(("UPDATE [dbo]."+userglobal+"_rosters SET [description] = '"+descriptions[q]+"' WHERE [roster_name] LIKE '%"+descriptions[z]+"%';"))
        q += 2
        z += 2
        if z >= len(descriptions):
            break

    conn.commit()#commits changes to the database
#--DELETES DESIRED ROSTER   (NEEDS A REWORK AT SOME POINT)----------------------
def del_rosters(val):
    the_user = (str(actualuser[0]+"_rosters"))
    if val in rosters:
        rosters.remove(val)
    i = 0
    while True:
        if indexable_rosters[i][0] == val:
            indexable_rosters.pop(i)
            break
        else:
            i += 1
            if i >= len(indexable_rosters):
                break
    cursor.execute("DELETE FROM "+the_user+" WHERE roster_name = '"+val+"'")
    conn.commit()
    indexable_rosters.clear()
    rosters.clear()
    rosters.append("MY QUIZZES")
    logged_in()
#--ENCAPSULATES ENTRY FIELDS IN "[]" IN PREP FOR SQL QUERY----------------------
def formatList(s):
    str1 = ""
    str2 = "], "
    str3 = "["
    for ele in s:
        str1 += (str3 + ele + str2)
    str1 = str1[:-2]
    return str1





#-----BUILDING NEW WINDOW TO DISPLAY AVAILABLE QUIZZES--------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
def find_quiz():
    findquiz_window = Toplevel()
    findquiz_window.title("AVAILABLE QUIZZES")
    findquiz_window.geometry("1210x590")
    findquiz_window.configure(bg='gray86')

    usrnm = Label(findquiz_window, text="---TO TAKE A QUIZ SELECT ANY OF THE AUTHORS LISTED BELOW "+
    "TO REVEAL THEIR CREATED QUIZZES---", pady=10, bg='gray86')
    usrnm.config(font=("fixedsys", 12))
    usrnm.grid(row=0, column=0, sticky = 'e')


#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------





#--IF RETURNING USER, GRABS ROSTERS SPECIFIC TO THE USER FROM THE SERVER--------
def logged_in():
    if len(actualuser) == 0:
        return
    else:
        potential_user = pd.read_sql_query("Select * from INFORMATION_SCHEMA.TABLES", conn)
        tcount = len(potential_user.index)
        i = 0
        while True:
            user_tables.append(potential_user['TABLE_NAME'].values[i])
            i += 1
            if i >= tcount:
                break
        if str(actualuser[0]) + "_rosters" in user_tables:
            user_table_name = str(actualuser[0]) + "_rosters"
            user_rosters = pd.read_sql_query("Select * from " +user_table_name, conn)
            acount = len(user_rosters.index)
            j = 0
            while True and acount > 0:
                fixit = (user_rosters['roster_name'].values[j])
                if fixit not in rosters:
                    rosters.append(fixit)
                    indexable_rosters.append([user_rosters['roster_name'].values[j]])
                    j += 1
                else:
                    if user_rosters['roster_name'].values[j] in rosters:
                        j +=1
                if j >= acount:
                    break
            y = 0
            while True:
                smt = rosters[y].replace(" ", "")
                rosters.pop(y)
                rosters.insert(y, smt)
                y += 1
                if y >= len(rosters):
                    break
#this shit be important yo
            m = 0
            while True:
                k = 0
                l = 0
                while True and acount > 0:
                    if user_rosters['roster_name'].values[k] == indexable_rosters[m][0]:
                        indexable_rosters[m].append(user_rosters['Player Name'].values[k])
                    k += 1
                    if k >= acount:
                        break
                m += 1
                if m >= len(indexable_rosters):
                    break
            s = 0
            while True and acount > 0:
                dafrst  = indexable_rosters[s][0].replace(" ", "")
                indexable_rosters[s].pop(0)
                indexable_rosters[s].insert(0, dafrst)
                s += 1
                if s >= len(indexable_rosters):
                    break
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Save Rosters", command=sav_rosters)
    delmenu = Menu(filemenu)
    #n = 0
    #while True:
        #delmenu.add_command(label = str(rosters[0]), command=lambda:del_rosters(rosters[n]))
        #n += 1
        #if n >= len(rosters):
        #    break
    if len(rosters) == 1:
        delmenu.add_command(label = str(rosters[0]), command=lambda:del_rosters(rosters[0]))
    if len(rosters) == 2:
        delmenu.add_command(label = str(rosters[0]), command=lambda:del_rosters(rosters[0]))
        delmenu.add_command(label = str(rosters[1]), command=lambda:del_rosters(rosters[1]))
    if len(rosters) == 3:
        delmenu.add_command(label = str(rosters[0]), command=lambda:del_rosters(rosters[0]))
        delmenu.add_command(label = str(rosters[1]), command=lambda:del_rosters(rosters[1]))
        delmenu.add_command(label = str(rosters[2]), command=lambda:del_rosters(rosters[2]))
    if len(rosters) == 4:
        delmenu.add_command(label = str(rosters[0]), command=lambda:del_rosters(rosters[0]))
        delmenu.add_command(label = str(rosters[1]), command=lambda:del_rosters(rosters[1]))
        delmenu.add_command(label = str(rosters[2]), command=lambda:del_rosters(rosters[2]))
        delmenu.add_command(label = str(rosters[3]), command=lambda:del_rosters(rosters[3]))
    if len(rosters) == 5:
        delmenu.add_command(label = str(rosters[0]), command=lambda:del_rosters(rosters[0]))
        delmenu.add_command(label = str(rosters[1]), command=lambda:del_rosters(rosters[1]))
        delmenu.add_command(label = str(rosters[2]), command=lambda:del_rosters(rosters[2]))
        delmenu.add_command(label = str(rosters[3]), command=lambda:del_rosters(rosters[3]))
        delmenu.add_command(label = str(rosters[4]), command=lambda:del_rosters(rosters[4]))
    if len(rosters) == 6:
        delmenu.add_command(label = str(rosters[0]), command=lambda:del_rosters(rosters[0]))
        delmenu.add_command(label = str(rosters[1]), command=lambda:del_rosters(rosters[1]))
        delmenu.add_command(label = str(rosters[2]), command=lambda:del_rosters(rosters[2]))
        delmenu.add_command(label = str(rosters[3]), command=lambda:del_rosters(rosters[3]))
        delmenu.add_command(label = str(rosters[4]), command=lambda:del_rosters(rosters[4]))
        delmenu.add_command(label = str(rosters[5]), command=lambda:del_rosters(rosters[5]))
    if len(rosters) == 7:
        delmenu.add_command(label = str(rosters[0]), command=lambda:del_rosters(rosters[0]))
        delmenu.add_command(label = str(rosters[1]), command=lambda:del_rosters(rosters[1]))
        delmenu.add_command(label = str(rosters[2]), command=lambda:del_rosters(rosters[2]))
        delmenu.add_command(label = str(rosters[3]), command=lambda:del_rosters(rosters[3]))
        delmenu.add_command(label = str(rosters[4]), command=lambda:del_rosters(rosters[4]))
        delmenu.add_command(label = str(rosters[5]), command=lambda:del_rosters(rosters[5]))
        delmenu.add_command(label = str(rosters[6]), command=lambda:del_rosters(rosters[6]))
    if len(rosters) == 8:
        delmenu.add_command(label = str(rosters[0]), command=lambda:del_rosters(rosters[0]))
        delmenu.add_command(label = str(rosters[1]), command=lambda:del_rosters(rosters[1]))
        delmenu.add_command(label = str(rosters[2]), command=lambda:del_rosters(rosters[2]))
        delmenu.add_command(label = str(rosters[3]), command=lambda:del_rosters(rosters[3]))
        delmenu.add_command(label = str(rosters[4]), command=lambda:del_rosters(rosters[4]))
        delmenu.add_command(label = str(rosters[5]), command=lambda:del_rosters(rosters[5]))
        delmenu.add_command(label = str(rosters[6]), command=lambda:del_rosters(rosters[6]))
        delmenu.add_command(label = str(rosters[7]), command=lambda:del_rosters(rosters[7]))
    if len(rosters) == 9:
        delmenu.add_command(label = str(rosters[0]), command=lambda:del_rosters(rosters[0]))
        delmenu.add_command(label = str(rosters[1]), command=lambda:del_rosters(rosters[1]))
        delmenu.add_command(label = str(rosters[2]), command=lambda:del_rosters(rosters[2]))
        delmenu.add_command(label = str(rosters[3]), command=lambda:del_rosters(rosters[3]))
        delmenu.add_command(label = str(rosters[4]), command=lambda:del_rosters(rosters[4]))
        delmenu.add_command(label = str(rosters[5]), command=lambda:del_rosters(rosters[5]))
        delmenu.add_command(label = str(rosters[6]), command=lambda:del_rosters(rosters[6]))
        delmenu.add_command(label = str(rosters[7]), command=lambda:del_rosters(rosters[7]))
        delmenu.add_command(label = str(rosters[8]), command=lambda:del_rosters(rosters[8]))
    if len(rosters) == 10:
        delmenu.add_command(label = str(rosters[0]), command=lambda:del_rosters(rosters[0]))
        delmenu.add_command(label = str(rosters[1]), command=lambda:del_rosters(rosters[1]))
        delmenu.add_command(label = str(rosters[2]), command=lambda:del_rosters(rosters[2]))
        delmenu.add_command(label = str(rosters[3]), command=lambda:del_rosters(rosters[3]))
        delmenu.add_command(label = str(rosters[4]), command=lambda:del_rosters(rosters[4]))
        delmenu.add_command(label = str(rosters[5]), command=lambda:del_rosters(rosters[5]))
        delmenu.add_command(label = str(rosters[6]), command=lambda:del_rosters(rosters[6]))
        delmenu.add_command(label = str(rosters[7]), command=lambda:del_rosters(rosters[7]))
        delmenu.add_command(label = str(rosters[8]), command=lambda:del_rosters(rosters[8]))
        delmenu.add_command(label = str(rosters[9]), command=lambda:del_rosters(rosters[9]))

    filemenu.add_cascade(label="Delete A Roster",menu = delmenu)
    filemenu.add_command(label="About", command=donothing)
    filemenu.add_separator()
    filemenu.add_command(label="Exit Application", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    root.config(menu=menubar)
#--A FILLER FUNCTION------------------------------------------------------------
def donothing():
   x = 0
#-------------------------------------------------------------------------------
#
#               ______________       ___       ___              ____________
#             /  ___________  \      \  \      \  \            /____   ____/
#           /  /            \__\      \  \      \  \               /  /
#          /  /         _______        \  \      \  \              /  /
#          \  \         \____  \        \  \      \  \             /  /
#           \  \___________/  /          \  \______\  \         ___/  /_____
#            \_______________/            \____________\      /___________/
#
#----GUI BUILDING---------------------------------------------------------------
logged_in()   #checks to see if user has rosters saved

clicked = StringVar()
clicked.set("CHOOSE ONE")
selectby = Label(root, text="CREATE YOUR QUERY", pady=10, bg='gray86')
selectby.config(font=("fixedsys", 15))
selectby.grid(row=0, column=0,columnspan=2, sticky = 'nswe')
drop = OptionMenu(root, clicked, *searchable_list)
drop.grid(sticky='nswe')
drop["menu"].config(font=("fixedsys", 8), bg="gray86")
drop.config(width = 11, font=("fixedsys", 12),  bg='gray86',  bd=1, highlightbackground="light slate gray", highlightcolor="light slate gray", highlightthickness=2,relief='groove')
drop.grid(row=1, column=0, sticky='nswe', pady=5)

q = Entry(root, width=30, borderwidth=2, bg='gray70')
q.config(font=("fixedsys", 12))
q.grid(row=1, column=1, padx=10, pady=10)

create_roster = Label(root, text="BUILD A QUIZ", pady=10, bg='gray86')
create_roster.config(font=("fixedsys", 15))
create_roster.grid(row=0, column=3,columnspan=2, sticky = 'nswe')

rost_name = Label(root, text="QUIZ NAME:", pady=10, bg='gray86')
rost_name.config(font=("fixedsys", 14))
rost_name.grid(row=1, column=3, sticky = 'nswe')

n = Entry(root, width=30, borderwidth=2, bg='gray70')
n.config(font=("fixedsys", 12))
n.grid(row=1, column=4, padx=10, pady=10)

create_rost = Button(root,text="CREATE:", command=new_roster, bg='gray86')
create_rost.config(font=("fixedsys", 12))
create_rost.grid(row=1, column=5)

findquiz = Button(root,text="FIND A QUIZ:",command=find_quiz, bg='SeaGreen1')#command=find_quiz
findquiz.config(font=("fixedsys", 12))
findquiz.grid(row=1, column=6, columnspan=2, rowspan=2, sticky = 'nswe', padx=10)

player_name = Label(root, text="ADD PLAYER:", pady=10, bg='gray86')
player_name.config(font=("fixedsys", 14))
player_name.grid(row=2, column=3, sticky = 'nswe')

e = Entry(root, width=30, borderwidth=2, bg='gray70')
e.config(font=("fixedsys", 12))
e.grid(row=2, column=4, padx=10)
global searchbtn

searchbtn = Button(root,text="SEARCH:", command=card_builder, bg='gray86')
searchbtn.config(font=("fixedsys", 12))
searchbtn.grid(row=2, column=5)

clicker = StringVar()
clicker.set(rosters[0])
my_rosters = OptionMenu(root, clicker, *rosters)
my_rosters.grid(sticky='nswe')
my_rosters["menu"].config(font=("fixedsys", 8), bg="gray86")
my_rosters.config(width = 11, font=("fixedsys", 12),  bg='gray86',  bd=1, highlightbackground="light slate gray", highlightcolor="light slate gray", highlightthickness=2,relief='groove')
my_rosters.grid(row=5, column=3, columnspan=2, sticky='nswe', pady=5)

viewhbtn = Button(root,text="VIEW", command=view_roster, bg='light slate gray', bd=2, fg='gray90')
viewhbtn.config(font=("fixedsys", 12))
viewhbtn.grid(row=5, column=5, sticky='nswe', pady=5, padx=10)

clicked2 = StringVar()
clicked2.set(all_categories[0])
drop_cat = OptionMenu(root, clicked2, *all_categories)
drop_cat["menu"].config(font=("fixedsys", 8), bg="gray86")
drop_cat.config(font=("fixedsys", 12),  bg='gray86',  bd=1, highlightbackground="light slate gray", highlightcolor="light slate gray", highlightthickness=2,relief='groove')
drop_cat.grid(sticky='nwe',row=2, column=0)
loadbtn = Button(root,text="LOAD", command=load_query,anchor=NW, bg='light slate gray', fg="gray90")
loadbtn.config(font=("fixedsys", 12))
loadbtn.grid(row=2, column=1,sticky='nwe', padx = 5, pady = 5)

global query_frame
query_frame = LabelFrame(root, text="ADVANCED QUERY BUILDER", padx=5, pady=5, bg='gray86')
query_frame.grid(sticky='nswe')
query_frame.config(font=("fixedsys", 14))
query_frame.grid(row=4, column=0,rowspan=6,columnspan=2,  padx=10, pady=10)
q1 = Label(query_frame, text="Current Query:", bg='gray86')
q1.config(font=("fixedsys", 12))
q1.pack()

delbtn = Button(root,text="DELETE LAST", command=del_query,anchor=NW, bg='Salmon')
delbtn.config(width = 20, font=("fixedsys", 12))
delbtn.grid(row=10, column=0, sticky = 'nswe', padx=10, pady=5)
clrbtn = Button(root,text="CLEAR QUERY", command=del_qframe,anchor=NW, bg='Salmon')
clrbtn.config(width = 20, font=("fixedsys", 12))
clrbtn.grid(row=10, column=1, sticky = 'nswe', padx=10, pady=5)

runqry = Button(root,text="RUN QUERY", command=lambda:[adv_querysearch(),del_qframe()],anchor=NW, bg='khaki')
runqry.config(width = 20, font=("fixedsys", 12))
runqry.grid(row=12, column=0,columnspan=2, sticky = 'nswe', padx=10, pady=5)

col_spcr = Label(root, text='\t\t', bg='gray86')
col_spcr.grid(row=0, column=2)
col_spcr = Label(root, text='\t\t', bg='gray86')
col_spcr.grid(row=1, column=2)
col_spcr = Label(root, text='\t\t', bg='gray86')
col_spcr.grid(row=2, column=2)
col_spcr = Label(root, text='\t\t', bg='gray86')
col_spcr.grid(row=3, column=2)
col_spcr = Label(root, text='\t\t', bg='gray86')
col_spcr.grid(row=4, column=2)
col_spcr = Label(root, text='\t\t', bg='gray86')
col_spcr.grid(row=5, column=2)


#----------------
root.mainloop()#-----------------------------------------------------------------------------------------------------------=-=-=-=-=-=-=-=-=-----
#----------------
