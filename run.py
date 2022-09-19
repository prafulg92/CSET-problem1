from flask import Flask, jsonify
import pandas as pd
import numpy as np
import json
from treelib import Node, Tree
import sqlite3
import warnings
from flask_cors import CORS, cross_origin





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

if __name__ == '__main__':
   app.run('localhost', '5000', True)