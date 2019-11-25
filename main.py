from pip._vendor.distlib.compat import raw_input

import Querries

while(True):
    querry = raw_input("Type the number of query you wish to execute or 0 in order to exit: ")
    if querry=='1':
        Querries.Q1.execute()
    elif querry=='2':
        Querries.Q2.execute()
    elif querry=='3':
        Querries.Q3.execute()
    elif querry=='4':
        Querries.Q4.execute()
    elif querry=='5':
        Querries.Q5.execute()
    elif querry=='0':
        break
    else:
        print("You input was not recognized, please try again")


