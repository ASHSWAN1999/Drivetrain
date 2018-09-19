from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file as oauth_file, client, tools

from itertools import combinations_with_replacement

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

# The ID and range of a sample spreadsheet.
# SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
# SAMPLE_RANGE_NAME = 'Class Data!A2:E'
SAMPLE_SPREADSHEET_ID = '1Kx0QlxJy6_IUbmdS0-kOA1tjuJKSParKlkN3Q_79ZwA'
SAMPLE_RANGE_NAME = '1!A2:I18'
FW = 10
T = 76672
LOW_FOS = 4

MATRIX = []

GEAR_INDEX = []


def main():
    gears = ratio_combinations()
    #print(gears)
    GEAR_INDEX.extend(convert_to_indicies(gears))

    add_FoS_to_GEAR()
    print(GEAR_INDEX)
    good_combos = filter_gears()
    return good_combos

def retrieve_sheet(col):
    """Shows basic usage of the Sheets API.

    Prints values from a sample spreadsheet.
    """
    store = oauth_file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    result = service.spreadsheets().values().get(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    l = []
    if not values:
        print('No data found.')
    else:
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            # print(u'%s, %s' % (row[0], row[2]))
            l.append(row[col])
    return (l)


def make_matrix():
    for i in range(8):
        MATRIX.append(retrieve_sheet(i))

make_matrix()

def retrieve(col):
    return MATRIX[col]

def ratio_combinations():

    num_teeth = retrieve(0)
    print("num_teeth")

    min_ratio = 7.3
    max_ratio = 7.4

    viable_combos = []

    all_combos = combinations_with_replacement(num_teeth, 4)

    for i in all_combos:

        # 4th+2nd and 3rd+1st
        ratio1 = (int(i[3])/int(i[1]))*(int(i[2])/int(i[0]))
        if ratio1 > min_ratio and ratio1 < max_ratio:
            #viable_combos.append((ratio1, i[0], i[2], i[1], i[3]))
            print(ratio1, i[0], i[2], i[1], i[3])
            viable_combos.append([i[0], i[2], i[1], i[3]])
        # 4th+1sr and 3rd+2nd
        ratio2 = (int(i[3])/int(i[0]))*(int(i[2])/int(i[1]))
        if ratio2 > min_ratio and ratio2 < max_ratio:
            #viable_combos.append((ratio2, i[0], i[3], i[1], i[2]))
            print(ratio2, i[0], i[3], i[1], i[2])
            viable_combos.append([i[0], i[3], i[1], i[2]])

    return(viable_combos)
        # print(viable_combos)

def convert_to_indicies(gear_tooth_list):

    num_teeth = retrieve(0)
    row = {}
    for i in range(len(num_teeth)):
        row[num_teeth[i]] = i
    #print(dict)

    indicies_list =[]

    for i in gear_tooth_list:
        one_set = [0, 0, 0, 0]

        one_set[0] = row[i[0]]
        one_set[1] = row[i[1]]
        one_set[2] = row[i[2]]
        one_set[3] = row[i[3]]

        indicies_list.append(one_set)

    #print(indicies_list)
    return indicies_list

def FoS_given_T(combo, Torque, gear_num):
    # for i in GEAR_INDEX:
    #
    #combo = GEAR_INDEX[9]
    #Torque = T

    pitch_diameters = retrieve(6)
    diameter = int(pitch_diameters[combo[gear_num]])

    Wt = Torque/(diameter/2)

    teeth_num = retrieve(0)
    tooth_num = int(teeth_num[combo[gear_num]])

    P = tooth_num/diameter

    b = FW

    l_factors = retrieve(7)
    y = float(l_factors[combo[gear_num]])

    Stress = (Wt*P)/(b*y)
    FoS = Stress/460.9
    #print(FoS)
    return FoS

def FoS1(combo):
    FoS1 = round(FoS_given_T(combo, Torque=T, gear_num=0), 3)
    return FoS1

def FoS2(combo):
    teeth = retrieve(0)
    tooth1 = int(teeth[combo[0]])

    tooth2 = int(teeth[combo[1]])

    Torque = T * (tooth2/tooth1)

    FoS2 = round(FoS_given_T(combo, Torque, 1), 3)
    return FoS2

def FoS3(combo):
    teeth = retrieve(0)
    tooth1 = int(teeth[combo[0]])

    tooth2 = int(teeth[combo[1]])

    Torque = T * (tooth2/tooth1)

    FoS3 = round(FoS_given_T(combo, Torque, 2), 3)
    return FoS3

def FoS4(combo):
    teeth = retrieve(0)
    tooth1 = int(teeth[combo[0]])

    tooth2 = int(teeth[combo[1]])

    tooth3 = int(teeth[combo[2]])

    tooth4 = int(teeth[combo[3]])

    Torque = T * ((tooth2/tooth1)*(tooth4/tooth3))

    FoS4 = round(FoS_given_T(combo, Torque, 3), 3)
    return FoS4

def combo_FoS(combo):
    FoS_list = []
    FoS_list.append(FoS1(combo))
    FoS_list.append(FoS2(combo))
    FoS_list.append(FoS3(combo))
    FoS_list.append(FoS4(combo))
    #print(FoS_list)
    return FoS_list

def add_FoS_to_GEAR():
    for i in range(len(GEAR_INDEX)):
        #print(i)
        FoS_list = combo_FoS(GEAR_INDEX[i])
        GEAR_INDEX[i].extend(FoS_list)

    #print(GEAR_INDEX)

def filter_gears():

    bad_is = []
    good_combos = []
    for i in range(len(GEAR_INDEX)):
        combo = GEAR_INDEX[i]
        #print(combo)
        combo_counter = 0
        for j in range(4):
            if combo[j+4] < LOW_FOS:
                combo_counter += 1
        if combo_counter == 0:
            good_combos.append(combo)

    #GEAR_INDEX = good_combos
    #print(good_combos)
    return good_combos

def test():
    pitch_diameters = retrieve(6)
    pd = pitch_diameters[GEAR_INDEX[0][0]]
    print(pd)


if __name__ == '__main__':
    gc = main()
    print(gc)
    #test()
