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
SAMPLE_RANGE_NAME = '1!A2:D17'

GEAR_INDEX = []

def main():
    gears = ratio_combinations()
    #print(gears)
    convert_to_indicies(gears)

def retrieve(col):
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

    print(indicies_list)


if __name__ == '__main__':
    main()
