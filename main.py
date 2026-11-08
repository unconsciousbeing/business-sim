import sys
from tabulate import tabulate
import random
from faker import Faker

fake = Faker()
companies = [fake.company() for _ in range(1000)]

def main_menu(menu_list, header_line, actionline):
    new_menu_list = []
    for n in range(len(menu_list)):
        new_menu_list.append([f'{n+1}. ' + menu_list[n]])
    found = False
    while not found:
        print(tabulate(new_menu_list, headers=[header_line], tablefmt='fancy_outline'))
        action = input(actionline).lower()
        try:
            act = int(action)
        except ValueError:
            for a in range(len(menu_list)):
                if menu_list[a].lower() == action.lower():
                    act = a+1
                    found = True
        else:
            if act in range(len(new_menu_list)+1):
                found = True
        if not found:
            print("Select a valid option from the following.\n")
        else:
            break
    return act

class Company:
    def __init__(self):
        self.cash = 5000
        self.clients = []
        self.ap = 0

    def maintenance_costs(self):
        office_rent = 650
        insurance_cost = 150
        daily_costs = 20
        week_cost = (office_rent+insurance_cost+(daily_costs*7))
        self.cash -= week_cost
        print(tabulate(
            [[f'Office rent = ${office_rent} \nInsurance = ${insurance_cost} \n\
            Daily Maintenance (food, software) = ${daily_costs*7} (in week terms)']], tablefmt='rounded_grid', 
            headers=["WEEKLY MAINTENANCE BILL"]))

    def add_client(self, clientname, prospectcost):
        self.clients.append({"name": clientname, "status": ["prospect", prospectcost], "contract": {}})

    def make_contract(self, clientname):
        cmoney = 3000 + random.randint(-2,4)*500
        cdays =  5*random.randint(2,6)
        wcost = int(((cmoney/cdays)*2)*0.7)
        for i in self.clients:
            if i['name'] == clientname:
                i['contract'] = {"cdays": cdays, "cmoney": cmoney, "cwork": cdays, "wcost": wcost}
                i['status'] = 'contract'
        print("Contract made successfully!")
        print(tabulate([[f"Company Name: {clientname}"], [f"Contract Money: ${cmoney}"], [f"Deadline in {cdays} days"]], 
                       tablefmt='fancy_grid'),"\n")

    def deadline_check(self):
        remove = []
        for i in range(len(self.clients)):
            if self.clients[i]['status'] == 'contract':
                self.clients[i]['contract']['cdays'] -= 1                                              # fix THISSSSSSSSSSSSSSSSSSSSSSSS
                if self.clients[i]['contract']['cdays'] <=0:
                    print(tabulate([[f"Your contract with {self.clients[i]['name']} has come to an end."], 
                                    [f"Contract Money Lost: ${self.clients[i]['contract']['cmoney']}"]], 
                                tablefmt='rounded_outline', headers=['END OF CONTRACT']),"\n")
                    remove.append(i)
        for name in remove:
            self.clients.remove(name)

    def end_contract(self, clientname):
        for n in range(len(self.clients)):
            if self.clients[n]['name'] == clientname:
                print(tabulate([[f'Company Name: {clientname}'], [f'Contract Money Received: ${self.clients[n]['contract']['cmoney']}']], 
                                tablefmt='rounded_outline', headers=['CONTRACT COMPLETED']))
                print()
                self.cash += self.clients[n]['contract']['cmoney']
                remove = n
        self.clients.pop(n)

    def prospectfind(self): # 2 AP -> guaranteed prospect
        self.ap -= 2
        prospectlist = random.choices(companies, k=5)
        method = main_menu(['Organic Prospects', 'Quality Prospects (third party, paid with cash)'], 
                actionline='Which prospect method to use? ', header_line='PROSPECTING METHOD')
        print("\nSelect a company from the list:")
        for i in range(len(prospectlist)):
            print(f"{i+1}. {prospectlist[i]}")
        chance = random.randint(1,20)
        if chance in range(1,4):
            prospectcost = random.randint(2,4)
        elif chance in range(4,18):
            prospectcost = random.randint(4,8)
        elif chance in range(18,21):
            prospectcost = random.randint(8,12)
        if method == 2:
            prospectcost -= int(prospectcost/2)
            self.cash -= 50
        prospect_found = False
        while not prospect_found:
            prospectname = input("Which client would you like to work with? ")
            try:
                prospect = int(prospectname)
            except ValueError:
                for names in prospectlist:
                    if names.lower() == prospectname.lower():
                        prospectname = names
                        self.add_client(prospectname, prospectcost)
                        prospect_found = True
            else:
                for no in range(len(prospectlist)):
                    if no+1 == prospect:
                        prospectname = prospectlist[no]
                        self.add_client(prospectname, prospectcost)
                        prospect_found = True
            if not prospect_found:
                print("Invalid client name.")
            else:
                print(f"Prospect Client Selected: {prospectname}\n")

    def pitch_client(self): # 2 AP -> -1 prospectcost
        prospectlist = []
        for name in self.clients:
            if name['status'][0] == 'prospect':
                prospectlist.append(name['name'])
        if not prospectlist:
            print("No prospects available to pitch!\n")
            return
        client_found = False
        while not client_found:
            clientname = main_menu(prospectlist, actionline='Which client to pitch: ', header_line='PITCH CLIENTS')
            print(tabulate({'Basic Proposal': '$50', 'Customized Detailed Proposal': '$150'}.items(), tablefmt='rounded_outline',
                                    headers=['Method', 'Cost']))
            while True:
                method = input("Which method to pitch the client? ")
                try:
                    method = int(method)
                except ValueError:
                    if method.lower() == 'basic proposal':
                        method = 1
                    elif method.lower() == "customized detailed proposal":
                        method = 2
                if method == 2:
                    prospectmultiplier = 2
                    self.cash -= 150
                    break
                elif method == 1:
                    prospectmultiplier = 1
                    self.cash -= 50
                    break
                if method not in [1,2]:
                    print("Invalid method")
                

            for n in range(len(self.clients)):
                if n+1 == int(clientname):
                    clientname = self.clients[n]['name']
                    break
            for n in range(len(self.clients)):
                if self.clients[n]['name'] == clientname:
                    self.clients[n]["status"][1] -= prospectmultiplier
                    if self.clients[n]["status"][1] <= 0:
                        self.make_contract(clientname)
                    else:
                        print(f"\nPitched client: {clientname} \nNo success, try again! \n")
                    self.ap -= 2
                    client_found = True
            if not client_found:
                print("Client not found.\n")

    def client_work(self):  # 2 AP -> 2 days' work
        contract_clients = []
        contract_list = []
        for name in self.clients:
            if name['status'] == 'contract':
                contract_list.append(name['name'])
                contract_clients.append(name)
        if not contract_list:
            print("No client projects to work on!\n")
            return
        client_found = False
        while not client_found:
            clientname = main_menu(contract_list, actionline="Which client's project to work on? ", 
                                   header_line='CLIENT PROJECT WORK')
            for n in range(len(contract_clients)):
                if n+1 == int(clientname):
                    clientname = contract_clients[n]['name']
                    break
            for n in range(len(self.clients)):
                if self.clients[n]['name'] == clientname:
                    if self.clients[n]['status'] == 'contract':
                        client_found = True
                        print(tabulate([[f'Client Name: {clientname}'],[f'Project Work would cost ${self.clients[n]['contract']['wcost']}']], 
                                       tablefmt='rounded_outline', headers=['CLIENT WORK']))
                        self.cash -= self.clients[n]['contract']['wcost']
                        self.clients[n]["contract"]['cwork'] -= 2
                        self.ap -= 2
                        if self.clients[n]['contract']['cwork'] <= 0:
                            self.end_contract(clientname)

            if not client_found:
                print("Client not found.")

    def overview(self):
        main_list = ['Company',
                      'Clients',
                      'Projects',
                      '']
        clients_list = ['List of Clients',
                        'Current Contracts',
                        'Current Prospects',
                        'Specific Client Info']
        company_list = []
        option = main_menu(menu_list=main_list, header_line='SHOW STATISTICS', actionline='Select an option. ')
        if option == 1:
            action = main_menu(menu_list=company_list, header_line='COMPANY OVERVIEW', actionline='Select an option. ')
        elif option == 2:
            action = main_menu(menu_list=clients_list, header_line='CLIENTS OVERVIEW', actionline='Select an option. ')
            if action == 1:
                new_menu_list = []
                for n in range(len(self.clients)):
                    new_menu_list.append([f'{n+1}. ' + self.clients[n]['name']])
                print(tabulate(new_menu_list, headers=['LIST OF CLIENTS'], tablefmt='fancy_outline'))
            elif action == 2:
                new_menu_list = []
                for n in range(len(self.clients)):
                    if self.clients[n]['contract']:
                        new_menu_list.append([self.clients[n]['name'], f'{self.clients[n]['contract']['cdays']} days', 
                                              f'${self.clients[n]['contract']['cmoney']}'])
                        print(tabulate(new_menu_list, tablefmt='fancy_outline', headers=['Client Name', 'Days until Deadline', 
                                                                                         'Contract Amount']))
            elif action == 3:
                new_menu_list = []
                for n in range(len(self.clients)):
                    if self.clients[n]['status'][0] == 'prospect':
                        new_menu_list.append([f'{n+1}. '+self.clients[n]['name']])
                        print(tabulate(new_menu_list, tablefmt='fancy_outline', headers=['LIST OF PROSPECT CLIENTS']))
company = Company()
day = 1

while True:
    company.ap += 10
    overview_list = [[f"DAY {day}"], [f"Cash available: ${company.cash}"], [f"Action Points available: {company.ap}"]]
    print(tabulate(overview_list, tablefmt='rounded_outline'))
    print()
    action_list = ['Find prospects',
                   'Pitch a client',
                    'Work on a project',
                    'Overview',
                    'Exit',
                    'Next Day']
    while company.ap > 0:
        actt = main_menu(actionline="What would you like to do? ", menu_list=action_list, header_line="MAIN MENU")
        print()
        if actt == 1:
            company.prospectfind()
        elif actt == 2:
            company.pitch_client()
        elif actt == 3:
            company.client_work()
        elif actt == 4:
            company.overview()
        elif actt == 5:
            sys.exit("Thanks for playing the sim! I hope you enjoyed the experience.")
        elif actt == 6:
            break
        print(f"Action Points: {company.ap}")

    if (day/7).is_integer():
        company.maintenance_costs()      
    company.deadline_check()
    day += 1
    print()

"""
- AP is just for limiting the number of actions in a day
- money is what drives the main game

Maintenance:
- Office rent & Insurance [weekly] - 650+150
- Food & Software [daily] - 15+5
Monthly maintenance = $3760

AVG CLIENT CONTRACT
- 2-5K 
- 10-30 days
- 175/day
- avg 

Prospect Cost:
- normal with AP
- boosted with third party ($50)

Pitching Cost:
- normal 50
- custom 150 (cutting 2x prospectcost)
 
Client acquisition cost: 
- 3500$ for one project, 70% work cost - $2450, CAC - $375, net margin = $675 per project, 20 days maintenance = ~$2500
- but since one project can be done with 34 AP (3.4 days), maintenance cost becomes $450, net profit per project becomes = $225
    
What to do next:
- Office space choice 
- save game (csv)
- Better UX **
- Make more use of money; maintenance cost; extra bonuses (pitching boost, client work boost)
- Progress bar for client work
- Add stats (info about clients, contract details only, current project progress, etc)  
- make an instructions menu option and show it at the beginning too

Issues to deal with first:

"""