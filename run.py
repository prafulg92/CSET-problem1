from flask import Flask, jsonify
import pandas as pd
import numpy as np
import json
from treelib import Node, Tree
import sqlite3
import warnings
from flask_cors import CORS, cross_origin
from treelib import Node, Tree
import sqlite3

tree = Tree()
seat_tree = Tree()





app = Flask(__name__)
CORS(app)

warnings.filterwarnings('ignore')
data=pd.read_csv("Office_OE_CODE.csv")
#seat=pd.read_csv("seat_mapping2.csv")
seat=pd.read_csv("seat_mapping3.csv")
seat_booking=pd.read_csv("seat_booking_dates.csv")


flr_df = pd.read_csv("floor.csv")

@app.route('/get_seat_allocation1/<oe_code>')
def seat_allocation1(oe_code):
    flr_wing_capacity_df = flr_df.groupby(['floor', 'wing'])['seatno'].count()
    flr_wing_capacity_df = flr_wing_capacity_df.reset_index()
    flr_wing_capacity_df = flr_wing_capacity_df.rename(columns={'seatno': 'total_seat'})

    var_jason = {}
    var_jason['L1'] = {
        "product_id": int(46539040),
        "freeSeating": False,
        "tempTransId": "1ecae165f2d86315fea19963d0ded41a",
        "seatLayout": {
            "colAreas": {
                "Count": int(4),
                "intMaxSeatId": 0,
                # flr_wing_capacity_df.groupby(['floor'])['total_seat'].sum()['L1'],
                "intMinSeatId": int(2),
                "objArea": []
            }
        }
    }

    var_jason['L2'] = {
        "product_id": int(46539041),
        "freeSeating": False,
        "tempTransId": "1ecae165f2d86315fea19963d0ded41b",
        "seatLayout": {
            "colAreas": {
                "Count": int(4),
                "intMaxSeatId": 0,
                "intMinSeatId": int(2),
                "objArea": []
            }
        }
    }

    var_jason['L3'] = {
        "product_id": int(46539042),
        "freeSeating": False,
        "tempTransId": "1ecae165f2d86315fea19963d0ded41c",
        "seatLayout": {
            "colAreas": {
                "Count": int(4),
                "intMaxSeatId": 0,
                "intMinSeatId": int(2),
                "objArea": []
            }
        }
    }

    var_jason['L4'] = {
        "product_id": int(46539043),
        "freeSeating": False,
        "tempTransId": "1ecae165f2d86315fea19963d0ded41d",
        "seatLayout": {
            "colAreas": {
                "Count": int(4),
                "intMaxSeatId": 0,
                "intMinSeatId": int(2),
                "objArea": []
            }
        }
    }

    print(flr_wing_capacity_df)
    for i in range(len(flr_wing_capacity_df)):
        flr = flr_wing_capacity_df['floor'][i]
        var_jason[flr]['seatLayout']['colAreas']['intMaxSeatId'] = int(
            flr_wing_capacity_df.groupby(['floor'])['total_seat'].sum()[flr])
        var_jason[flr]['seatLayout']['colAreas']['intMaxSeatId'] = 30
        wings = flr_wing_capacity_df['wing'][i]
        wing_index = 0

        if wings == 'A':
            wing_index = 0
        elif wings == 'B':
            wing_index = 1
        elif wings == 'C':
            wing_index = 2
        else:
            wing_index = 3

        count = flr_wing_capacity_df['total_seat'][i]
        var_jason[flr]['seatLayout']['colAreas']['objArea'].append({
            "AreaDesc": "Wing " + wings,
            "AreaCode": "0000000003",
            "AreaNum": "1",
            "HasCurrentOrder": True,
            "objRow": [
                {
                    "GridRowId": '1',
                    "PhyRowId": "A",
                    "objSeat": []
                },
                {
                    "GridRowId": '2',
                    "PhyRowId": "B",
                    "objSeat": []
                }
            ]
        })

        rowseat = []
        for j in range(count):
            seatNumber = j+1
            if j > 19:
                seatNumber = seatNumber-20
                GridSeatNum = seatNumber
                if j > 29:
                    GridSeatNum = seatNumber+5
                # elif seatNumber%5 == 1:
                #     GridSeatNum = seatNumber+1
            else:
                GridSeatNum = seatNumber
                if j > 9:
                    GridSeatNum = seatNumber+5
                # elif seatNumber%5 == 1:
                #     GridSeatNum = seatNumber+1            
            rowseat.append({
                "GridSeatNum": GridSeatNum,
                "SeatStatus": "0",
                # "seatNumber": str(flr) + wings + str(j+1)
                "seatNumber": seatNumber
            })

            if j == 19:
                var_jason[flr]['seatLayout']['colAreas']['objArea'][wing_index]['objRow'][0]['objSeat'] = rowseat
                rowseat = []
            else:
                var_jason[flr]['seatLayout']['colAreas']['objArea'][wing_index]['objRow'][1]['objSeat'] = rowseat

    return jsonify(var_jason)


@app.route('/get_seat_allocation/<oe_code>')
def seat_allocation(oe_code):
    seat_allocated = pd.read_csv('seat_mapping3.csv')
    # seat_allocated = seat_allocated[seat_allocated['Allocated'] != 'Not Applicable']
    # print(seat_allocated)
    # df = seat_allocated[['Manager_OE_Code', 'Manager_Dept', 'floor', 'wing', 'seat_no']]
    # df = seat_allocated.reset_index()
    df = seat_allocated

    df = df.groupby(['floor', 'wing'])['seat_no'].count()
    df = df.reset_index()
    df = df.rename(columns={'seatno': 'total_seat'})
    
    var_jason = {}
    var_jason['L1'] = {
        "product_id": int(46539040),
        "freeSeating": False,
        "tempTransId": "1ecae165f2d86315fea19963d0ded41a",
        "seatLayout": {
            "colAreas": {
                "Count": int(4),
                "intMaxSeatId": 0,
                # flr_wing_capacity_df.groupby(['floor'])['total_seat'].sum()['L1'],
                "intMinSeatId": int(2),
                "objArea": []
            }
        }
    }

    var_jason['L2'] = {
        "product_id": int(46539041),
        "freeSeating": False,
        "tempTransId": "1ecae165f2d86315fea19963d0ded41b",
        "seatLayout": {
            "colAreas": {
                "Count": int(4),
                "intMaxSeatId": 0,
                "intMinSeatId": int(2),
                "objArea": []
            }
        }
    }

    var_jason['L3'] = {
        "product_id": int(46539042),
        "freeSeating": False,
        "tempTransId": "1ecae165f2d86315fea19963d0ded41c",
        "seatLayout": {
            "colAreas": {
                "Count": int(4),
                "intMaxSeatId": 0,
                "intMinSeatId": int(2),
                "objArea": []
            }
        }
    }

    var_jason['L4'] = {
        "product_id": int(46539043),
        "freeSeating": False,
        "tempTransId": "1ecae165f2d86315fea19963d0ded41d",
        "seatLayout": {
            "colAreas": {
                "Count": int(4),
                "intMaxSeatId": 0,
                "intMinSeatId": int(2),
                "objArea": []
            }
        }
    }

    print(df)
    for i in range(len(df)):
        if df['floor'][i] == 'EO':
            continue
        flr = df['floor'][i]
        # var_jason[flr]['seatLayout']['colAreas']['intMaxSeatId'] = int(
        #     df.groupby(['floor'])['Manager_OE_Code'].count()[flr])
        var_jason[flr]['seatLayout']['colAreas']['intMaxSeatId'] = 30
        wings = df['wing'][i]
        wing_index = 0

        if wings == 'A':
            wing_index = 0
        elif wings == 'B':
            wing_index = 1
        elif wings == 'C':
            wing_index = 2
        else:
            wing_index = 3

        # count = df['seat_no'][i]
        count = len(seat_allocated[(seat_allocated['floor']==df['floor'][i]) & (seat_allocated['wing']==df['wing'][i])])
        print('seat details', seat_allocated[(seat_allocated['floor']==df['floor'][i]) & (seat_allocated['wing']==df['wing'][i])].iloc[0])
        var_jason[flr]['seatLayout']['colAreas']['objArea'].append({
            "AreaDesc": "Wing " + wings,
            "AreaCode": "0000000003",
            "AreaNum": "1",
            "HasCurrentOrder": True,
            "objRow": [
                {
                    "GridRowId": '1',
                    "PhyRowId": "A",
                    "objSeat": []
                },
                {
                    "GridRowId": '2',
                    "PhyRowId": "B",
                    "objSeat": []
                }
            ]
        })

        rowseat = []
        for j in range(count):
            seatDetails = seat_allocated[(seat_allocated['floor']==df['floor'][i]) & (seat_allocated['wing']==df['wing'][i])].iloc[j]
            seatNumber = j + 1
            if j > 19:
                seatNumber = seatNumber - 20
                GridSeatNum = seatNumber
                if j > 29:
                    GridSeatNum = seatNumber + 5
                # elif seatNumber%5 == 1:
                #     GridSeatNum = seatNumber+1
            else:
                GridSeatNum = seatNumber
                if j > 9:
                    GridSeatNum = seatNumber + 5
                # elif seatNumber%5 == 1:
                #     GridSeatNum = seatNumber+1
            rowseat.append({
                "GridSeatNum": GridSeatNum,
                "SeatStatus": "0",
                # "seatNumber": str(flr) + wings + str(j+1)
                "seatNumber": seatNumber,
                "department": str(seatDetails['Manager_Dept']),
                "Manager_OE_Code": str(seatDetails['Manager_OE_Code']),
                "number": seatDetails['seat_no'],  # seatNumber
            })

            if j == 19:
                var_jason[flr]['seatLayout']['colAreas']['objArea'][wing_index]['objRow'][0]['objSeat'] = rowseat
                rowseat = []
            else:
                var_jason[flr]['seatLayout']['colAreas']['objArea'][wing_index]['objRow'][1]['objSeat'] = rowseat

    return jsonify(var_jason)

@app.route('/allocate_seat')
def allocate_seat():
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

if __name__ == '__main__':
   app.run('localhost', '5000', True)