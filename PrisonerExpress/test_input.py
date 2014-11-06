import xlrd
import json
import requests
import time
book = xlrd.open_workbook("data.xlsx")


sh = book.sheet_by_index(0)
for rx in range(sh.nrows):
        if rx == 0:
                continue
        payload = { 'first_name': sh.row(rx)[0].value,'last_name':sh.row(rx)[1].value, 'id':sh.row(rx)[2].value, 'preaddr':sh.row(rx)[3].value,
				'addr':sh.row(rx)[4].value, 'city':sh.row(rx)[5].value, 'state':sh.row(rx)[6].value, 'zipcode':sh.row(rx)[7].value}
        print payload
        r = requests.get("http://localhost:8000/fast_input",params=payload)
        print r.text
        time.sleep(2)




