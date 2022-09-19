import pandas as pd
import numpy as np
from treelib import Node, Tree
import sqlite3
import warnings
warnings.filterwarnings('ignore')
data=pd.read_csv("Office_OE_CODE.csv")
#seat=pd.read_csv("seat_mapping2.csv")
seat=pd.read_csv("seat_mapping3.csv")
seat_booking=pd.read_csv("seat_booking_dates.csv")

tree = Tree()
seat_tree = Tree()

def create_employee_org(data) :
    if len(tree.nodes)==0 :
        tree.create_node("Employee Org", 0)
        # Creating nodes under root
        for i, c in data.iterrows():
            tree.create_node(c[1],c[0], parent=0,data=c[["Emp_OE_Code","Manager_OE_Code","Manager_Dept","Emp_ID"]])
        # Moving nodes to reflect the parent-child relationship
        for i, c in data.iterrows():
            if c["Manager_OE_Code"] == c["Manager_OE_Code"]:
                tree.move_node(c[0], c["Manager_OE_Code"])
                
def create_seat_mapping(seat_data):
    if len(seat_tree.nodes)==0 :
        seat_tree.create_node("Seat Catalogue", 0)
        # Creating nodes under root
        for i, c in seat.iterrows():
            seat_tree.create_node(c["Child"], c["Child"], parent=0,data=c["Allocated"])
        # Moving nodes to reflect the parent-child relationship
        for i, c in seat.iterrows():
            if c["Parent"] == c["Parent"]:
                seat_tree.move_node(c["Child"], c["Parent"])

def view_seat_booked_dates(Employee_ID) : # (String)
    pd.options.mode.chained_assignment = None
    manger_oe_code=tree.parent(Employee_ID).data.Emp_ID # 'OEA11_1' => Employee_ID
    mgn_allocated_seat=seat_data.query("Manager_OE_Code=='"+manger_oe_code+"'")
    seats_allocated=mgn_allocated_seat.Child.to_list()
    dates=seat_booking.query("seat_no in (" + ",".join("'{0}'".format(w) for w in seats_allocated) + ")") 
    dates["Level"]=dates["seat_no"].str[:2]
    dates["Wing"]=dates["seat_no"].str[2]+dates["seat_no"].str[1]
    dates["Seat_seq"]=dates["seat_no"].str[3:]
    return dates

def book_seat(Employee_ID, Dates,seat_no) : # (String,List of Dates in DD-Mon-YYYY formate,String)
    pd.options.mode.chained_assignment = None
    Dates=",".join("'{0}'".format(w) for w in Dates)
    manger_oe_code=tree.parent('OEA11_1').data.Emp_ID # 'OEA11_1' => Employee_ID
    mgn_allocated_seat=seat.query("Manager_OE_Code=='"+manger_oe_code+"'")
    dates_booked=seat_booking.query("seat_no=='"+seat_no+"' and Date_booked in (" +Dates +")")
    if len(dates_booked)==0 and seat_no in list(mgn_allocated_seat.Child):
        for dt in Dates:
            seat_booking.append={'seat_no':seat_no, 'Date_booked':dt, 'Emp_ID':Employee_ID}
        seat_booking.to_csv("seat_booking_dates.csv")
        print("Seat Booked")
        return True
    else:
        print("Seat can not be booked, either seat is already booked or seat is not allocated to your OE code")
        return False

def print_seat_allocation():
    for F in seat_tree.children('EON2'):
        print(F.tag)
        for wing in seat_tree.children(F.tag) :
            print("..."+wing.tag)
            for loc in seat_tree.children(wing.tag) :
                print("......"+str(loc))

def condition(x):
    if x=='EON2':
        return ""
    elif x in ['L1','L2','L3','L4']:
        return "EON2"
    elif x in ['A1','B1','C1','D1']:
        return 'L1'
    elif x in ['A2','B2','C2','D2']:
        return 'L2'
    elif x in ['A3','B3','C3','D3']:
        return 'L3'
    elif x in ['A4','B4','C4','D4']:
        return 'L4'
    elif len(x)>=4 :
        return x[2]+x[1]                
                
def convert_seat_data_to_df() :
    seat_data = pd.DataFrame(columns=['Child','Allocated'])
    seat_dic = {}
    for n in seat_tree.all_nodes_itr():
        temp_df = pd.DataFrame(columns=['Child','Allocated'])
        dl = {}
        if n.identifier!=0.0 :
            dl['Child'] = n.identifier
            if type(n.data) == str:
                dl['Allocated'] = n.data
            else:
                dl['Allocated'] = n.data
            t = temp_df.append(dl, ignore_index=True)
            seat_data = seat_data.append(t, ignore_index=True)  
    seat_data["Emp_OE_Code"]=seat_data.Allocated.str.split(",").str[0]
    seat_data["Manager_OE_Code"]=seat_data.Allocated.str.split(",").str[1]
    seat_data["Manager_Dept"]=seat_data.Allocated.str.split(",").str[2]
    seat_data["Emp_ID"]="" #seat_data.Allocated.str.split(",").str[3]
    seat_data['Parent']=seat_data['Child'].apply(condition)
    seat_data=seat_data[['Parent','Child','Allocated','Emp_OE_Code', 'Manager_OE_Code',
       'Manager_Dept', 'Emp_ID']]
    return seat_data     

def split_seat_count(max_size,seat) :
    lst=[]
    if max_size>0 :
        print("max_size :",max_size," seat :",seat)
        last_chunk=seat % max_size
        parts=int(np.floor(seat/max_size))
        for j in range(parts):
            lst.append(max_size)
        lst.append(last_chunk)
        print(lst)
        return lst
    else :
        print("max_size :",max_size," seat :",seat)
        return lst

def check_floor_wing_availability(seat_no,df,dept_list):
    conn = sqlite3.connect(':memory:')  
    cursor= conn.cursor()
    data=df.copy()
    vaccancy_df=pd.DataFrame()
    seat_clusteting=data.query("Emp_OE_Code != 'Not Applicable'")[['Parent','Child','Emp_OE_Code','Manager_OE_Code',
       'Manager_Dept','Emp_ID']]
    seat_clusteting["Level"]=seat_clusteting["Child"].str[:2]
    seat_clusteting["Wing"]=seat_clusteting["Child"].str[2]+seat_clusteting["Child"].str[1]
    seat_clusteting["Seat_No"]=seat_clusteting["Child"].str[3:]
    tbl=cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='seat_clusteting'").fetchall()
    if len(tbl)>0 :
        cursor.execute("Drop table seat_clusteting")
    seat_clusteting.to_sql(name='seat_clusteting', con=conn, index=False)
    sql="""Select max(vacant_seats) max_vacant_seats from
           (Select Level,Wing,sum(case when Emp_OE_Code=='0' then 1 else 0 end ) vacant_seats
             from seat_clusteting group by Level,Wing)"""   
    max_vacant_seats=pd.read_sql(sql, con=conn).values[0][0]
    seat_no_list=split_seat_count(max_vacant_seats,seat_no)
    for vac in seat_no_list:
        sql="""WITH X AS (Select Level,Wing,vacant_seats,Manager_Dept,dept_seats FROM 
                      (Select Level,Wing,Manager_Dept,
                              count(1) total_seats,
                              sum(case when Emp_OE_Code<>'0' then 1 else 0 end ) allocated_seats,
                              sum(case when Emp_OE_Code=='0' then 1 else 0 end ) vacant_seats,
                              sum(case when Manager_Dept in (""" + dept_list +""")  then 1 else 0 end ) dept_seats
                       from seat_clusteting
                       group by Level,Wing,Manager_Dept))
               Select Level,Wing,vacant_seats from X WHERE (Level,Wing) in 
                      (Select Level,Wing from X WHERE dept_seats>0 ) and vacant_seats>=round(""" + str(vac) + """,0)
               Union All
               Select Level,Wing,vacant_seats from X 
                WHERE dept_seats==0 and vacant_seats>=round(""" + str(vac) + """,0)
           """ 
        temp=pd.read_sql(sql, con=conn)
        temp=temp.drop_duplicates(keep='first')
        temp=pd.concat([temp,vaccancy_df])
        temp.reset_index(inplace=True,drop=True)
        temp=temp.drop_duplicates(keep=False)
        vaccancy_df=vaccancy_df.append(temp.head(1))
    cursor.close()
    conn.close()
    return vaccancy_df

def validate_quota(subtree):
    print("....Validating a quota for " + str(subtree.root))
    oe_code_list=[]
    oe_code_count=subtree.size()
    for n in subtree.all_nodes_itr():
        if len(n.data)>1:
            oe_code_list.append(n.data[0])
            # "Emp_OE_Code","Manager_OE_Code","Manager_Dept","Emp_ID"
    seat_oe_code=[]
    for F in seat_tree.children('EON2'):
        for wing in seat_tree.children(F.tag) :
            for loc in seat_tree.children(wing.tag) :
                #print(".....",loc.data,len(loc.data),loc.data.split(",")[0])
                if len(loc.data)>1:
                     #seat_oe_code.append(loc.data.['Emp_OE_Code'])
                     #seat_oe_code.append(loc.data.get('Emp_OE_Code'))
                    seat_oe_code.append(loc.data.split(",")[0])
                    # "Emp_OE_Code","Manager_OE_Code","Manager_Dept","Emp_ID"
    reserved_seats=0
    for i in set(oe_code_list):
        reserved_seats=reserved_seats+seat_oe_code.count(i)
         
    if reserved_seats>=np.round(oe_code_count*0.65,0) :
        print("... Quota complete for "+ str(subtree.root))
        return False
    else:
        print("... Quota is not complete for "+ str(subtree.root))
        return True

def reserve_seats(subtree) :
    if validate_quota(subtree):
        if subtree.size()>1:
            reserve_seat=np.round(subtree.size()*0.65,0)
        else:
            reserve_seat=int(subtree.size())
            print("reserve_seat : ",reserve_seat)
        seat_df=convert_seat_data_to_df()
        print("Requesting ",reserve_seat," seats")
        dept_list=[]
        for n in subtree.all_nodes_itr():
                if len(n.data)>1:
                    dept_list.append(n.data[2].strip())
        dept_list=",".join("'{0}'".format(w) for w in list(set(dept_list)))
        vaccancy_df=check_floor_wing_availability(reserve_seat,seat_df,dept_list)
        if len(vaccancy_df) >0 :
            for i in subtree.all_nodes() :
                flag=0
                for F in seat_tree.children('EON2'):
                    if F.tag in vaccancy_df.Level.to_list():
                        for wing in seat_tree.children(F.tag) :
                            if wing.tag in vaccancy_df.Wing.to_list():
                                for loc in seat_tree.children(wing.tag) :
                                    if len(loc.data)==1 and reserve_seat>0:
                                        #loc.data=i.data
                                        loc.data=",".join(i.data)
                                        # "Emp_OE_Code","Manager_OE_Code","Manager_Dept","Emp_ID"
                                        reserve_seat=reserve_seat-1
                                        flag=1
                                        break
                                if flag==1:
                                    break
                        if flag==1:
                            break
                    if flag==1:
                        break
            return True
        else:
            print("There is no Vaccancy, checked all floors")
            return False
    else:
        return False
    
def main():
    create_employee_org(data)
    create_seat_mapping(seat)
    for E in tree.children('Dir'):
        subtree=tree.subtree(E.identifier)
        print(subtree.size())
        result=reserve_seats(subtree)
    seat_data=convert_seat_data_to_df()
    seat_data['floor'] = ''
    seat_data['wing'] = ''
    seat_data['seat_no'] = ''
    for i in range(len(seat_data)):
        if len(seat_data['Child'][i]) >= 3:
            seat_data['floor'][i] = seat_data['Child'][i][:2]
            seat_data['wing'][i] = seat_data['Child'][i][2:3]
            seat_data['seat_no'][i] = int(seat_data['Child'][i][3:])

    seat_data.to_csv("seat_mapping3.csv")
    #print(seat_tree.to_json(with_data=True))

main()