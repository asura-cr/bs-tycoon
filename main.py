import pyfiglet
import random 
from rich import print
from rich.console import Console
from rich.table import Table
import os
import pickle
import csv

def rent():
    global cash
    global day
    rent = 200 + 50*(day-1) # rent increases by AED 50 every day
    cash -= rent
    print("Rent paid: AED", rent)

def dailywage():
    global cash
    global staffcount
    cash -= staffcount*100
    print("Daily wages for staff: AED", staffcount*100)

def revenue():
    global cash
    global price
    global staffcount


    stay_fract=1 - 0.02*(price-10)# customers staying after price increase
    customerbase = int(max(0,(random.randint(10+5*staffcount,10+10*staffcount)*stay_fract)))

    revenue = price*customerbase
    cash += revenue
    return revenue

def save_game():
    global cash 
    global price
    global days_since_event
    global day
    global staffcount
    try:
        f = open("save.dat","wb")
        pickle.dump((cash, price, days_since_event, day, staffcount), f)
        f.close()
    except FileNotFoundError:
        print("Error: Save file not found.")
    except Exception as e:
        print(f"Error saving game: {e}")

def load_game():
    global cash 
    global price
    global days_since_event
    global day
    global staffcount
    try:
        f = open("save.dat","rb")
        cash, price, days_since_event, day, staffcount = pickle.load(f)
        f.close()
    except FileNotFoundError:
        print("No saved game found. Starting a new game.")
        cash = 1000
        price = 10
        days_since_event = 0
        day = 1
        staffcount = 1
    except Exception as e:
        print(f"Error loading game: {e}")
        cash = 1000
        price = 10
        days_since_event = 0
        day = 1
        staffcount = 1

def save_to_leaderboard():
    global cash
    global day
    name = input("Enter your name for the leaderboard: ")
    try:
        with open("leaderboard.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([name, cash, day])
    except Exception as e:
        print(f"Error writing to leaderboard: {e}")

def load_leaderboard():
    try:
        with open("leaderboard.csv", "r") as f:
            reader = csv.reader(f)
            leaderboard = sorted(reader, key=lambda x: int(x[1]), reverse=True)
            return leaderboard
    except FileNotFoundError:
        print("No leaderboard found.")
        return []
    except Exception as e:
        print(f"Error loading leaderboard: {e}")
        return []

def delete_save():
    try:
        os.remove("save.dat")
    except FileNotFoundError:
        print("No save file found to delete.")
    except Exception as e:
        print(f"Error deleting save file: {e}")
def random_event():
    global cash
    global price
    global days_since_event
    days_since_event = 0
    amt=random.randint(10,80) * cash//100

    event_type=random.choice(['positive','negative'])
    positive_events=['You had payed more than required taxes and got a refund of {amt}','you were found doing good deeds and got a reward of {amt}','you received a grant from the government of {amt}','the supplier gave you a discount of {amt} as a gesture of goodwill for the years of trade']
    negative_events=['You were found doing tax fraud and had to pay a fine of {amt}','your store was robbed and you lost {amt}','the supplier increased the price of goods and you had to pay an extra {amt}','you were found doing illegal trade and had to pay a fine of {amt}','A natural disaster struck and you had to pay {amt} for repairs']

    if event_type=='positive':
        event = random.choice(positive_events)
        cash += amt
        print("Random Event: ")
        print(event.format(amt=amt))
        print()
    else:
        event = random.choice(negative_events)
        cash -= amt
        print("Random Event: ")
        print(event.format(amt=amt))
        print()

console = Console()


days_since_event = 0 # random event counter to ensure random events happen every 3 days
cash = 1000
day = 1 
price = 10
staffcount = 1

if os.path.exists("save.dat") == True:
    load=input("Continue saved game? (y/n): ")
    if load.lower() == "y":
        load_game()
        print("Continuing saved game...")
    else:
        print("Starting a new game...")
    

console.print(pyfiglet.figlet_format("STARTUP TYCOON"), style="bold red")
print("Welcome to Startup Tycoon!")
print()
print("You're running a small business with AED 1000 in starting capital.")
print("Your goal: survive 15 days without going bankrupt.")
print()
print("Each day you can choose ONE action:")
print("  - Hire staff (costs AED 500 upfront + AED 100/day wages, boosts your customer base)")
print("  - Fire staff (reduces wages, but also reduces sales potential)")
print("  - Change your price (higher price = more profit per sale, but fewer customers)")
print("  - Skip and end the day (no changes, just move on)")
print()
print("At the end of each day, you'll pay rent and wages, and earn revenue based on your price and staff count.")
print("Watch out for random events, they can boost or drain your cash unexpectedly.")
print("Balance your price, staff, and cash carefully. Good luck!")
print()
input("Press Enter to start your business...")

while True:
    
    if day<=15 and cash>0:
        
        console.print(pyfiglet.figlet_format("D A Y - "+str(day)),style = "bold red")
        stats_table=Table(title="Business Stats", show_header=True, header_style="bold green", border_style="bold cyan")

        stats_table.add_column("Day", justify="center", style=" bold yellow")
        stats_table.add_column("Cash", justify="center", style="bold yellow")
        stats_table.add_column("Price", justify="center",style="bold yellow")
        stats_table.add_column("Staff Count", justify="center",style="bold yellow")

        stats_table.add_row(str(day), "AED"+ str(cash), "AED"+ str(price), str(staffcount))

        console.print(stats_table)
        print()


        console.print(pyfiglet.figlet_format("GAME MENU"),style = "bold red")
        print("1. Hire Staff")
        print("2. Fire Staff")
        print("3. Change Price")
        print("4. Skip and End Day")
        print()
        choice = int(input("Enter your choice: "))
        if choice == 1:
            no=int(input("Enter number of staff to hire (each staff costs AED500 upfront and AED100 daily wages): "))
            if no>0:
                staffcount += no
                cash -= no*500 
                print("You hired ", no, " staff members.")
            else:
                print("Invalid number of staff to hire.")
                continue
            input("Press Enter to continue...")
        elif choice == 2:
            no=int(input("Number of staff to fire: "))
            if no>staffcount:
                print("You don't have that many staff members.")
                continue
            if no<0:
                print("Invalid number of staff to fire.")
                continue
            else:
                staffcount -= no
                print("You fired ", no, " staff members.")
                input("Press Enter to continue...")
    
        elif choice == 3:
            price=int(input("Enter new price: "))
            if price == 0 or price < 0:
                print("Price cannot be zero or negative. Please try again.")
                continue
            print("Price changed to AED", price)
            input("Press Enter to continue...")

        elif choice == 4:
            print("Skipping and ending  day ", day)
            input("Press Enter to continue...")
        else:
            print("Invalid choice. Please try again.")
            continue

        rent()
        dailywage()
        rev = revenue()
        print("Revenue for day ", day, ": AED", rev)
        print()



        if days_since_event < 3:
            if random.random() <0.3: # 30% chance of random event happening
                random_event()
        elif days_since_event >=3:
            random_event()

        input("Press Enter to continue...")


        days_since_event += 1
        day += 1 #increase day
        if day<=15 and cash>0:
            save_game()

        
            

    elif day>15 and cash>0:
        console.print(pyfiglet.figlet_format("CONGRATULATIONS!"), style = "bold green")
        print("You have successfully completed 15 days of business without going bankrupt.")
        print("You have completed 15 days of business.")
        print("Final balance: ", cash)
        save_to_leaderboard()
        delete_save()
        break
    else:
        delete_save()
        console.print(pyfiglet.figlet_format("GAME OVER"))
        print("You have gone bankrupt on day ", day-1)
        break

print("Leaderboard:")
for entry in load_leaderboard():
    print(f"{entry[0]}: AED{entry[1]} (Day {entry[2]})")