class Submarine:
    ''' -------------------
        Test Documentation
        นี่คือโปรแกรมสำหรับเรือดำน้ำ
        -------------------
    '''
    def __init__(self,price=10000,budget=100000):
        
        self.captain = 'pravit'
        self.sub_name = 'Uncle I'
        self.price = price
        self.kilo = 0
        self.budget = budget
        self.totalcost=0

    def Missile(self):
        print("we are Department of Missile")

    def Calcommission(self):
        ''' '''
        
        percent = self.price * (10/1000)
        print('Loong you got: {} Million baht'.format(percent))
    def Goto(self,enemypoint,distance):
        print(f"Let's go to {enemypoint} distance :{distance} KM")
        self.kilo= self.kilo+distance
        self.Fuel()

    def Fuel(self):
        deisel = 20
        cal_fuel_cost = self.kilo*deisel
        print('Current Feul Cost :{:,d} Baht'.format(cal_fuel_cost))
        self.totalcost += cal_fuel_cost
    @property
    def BudgetRemaining(self):

        remaining = self.budget-self.totalcost
        print('Budget Remaining : {:,.2f} Baht'.format(remaining))
        return remaining

class ElectricSubmarine(Submarine):
    def __init__(self,price=10000,budget=100000):
        self.sub_name= 'Uncle III'
        self.batter_distance =100000
        super().__init__(price,budget)
    
    def Battery(self):
       allbattery  = 100
       calculate = (self.kilo / self.batter_distance)*100
       print('We have battery :{} %'.format(allbattery-calculate))

    def Fuel(self):
        kilowatcost = 5
        cal_fuel_cost = self.kilo*kilowatcost
        print('Current Power Cost :{:,d} Baht'.format(cal_fuel_cost))
        self.totalcost += cal_fuel_cost

print(__name__)
if __name__ == "__main__":
    tesla = ElectricSubmarine(40000,2000000)
    print(tesla.captain)
    print(tesla.budget)
    tesla.Goto("japan",10000)
    print(tesla.BudgetRemaining)
    tesla.Battery()
    print('------------------')
    kongtabreuw = Submarine(40000,2000000)
    print(kongtabreuw.captain)
    print(kongtabreuw.budget)
    kongtabreuw.Goto("japan",10000)
    print(kongtabreuw.BudgetRemaining)


    # kongtabreuw = Submarine(20000)
    # print(kongtabreuw.captain)
    # print(kongtabreuw.sub_name)
    # print('----------------')
    # print(kongtabreuw.kilo)
    # kongtabreuw.Goto('China',70000)
    # print(kongtabreuw.kilo)
    # kongtabreuw.Fuel()
    # current_budget =kongtabreuw.BudgetRemaining
    # print(current_budget * 0.2)
    # kongtabreuw.Calcommission()

    # print('--------sub no.2 --------')
    # kongtabbok = Submarine(30000)
    # kongtabbok.captain='srevara'
    # print(kongtabbok.captain)



        
