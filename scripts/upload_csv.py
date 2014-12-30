from PrisonerExpress.models import Prisoner, Address
import re, string, time
from datetime import datetime
import csv

def read_file(fname):
    with open(fname, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        header = {}
        pattern = re.compile('[\W_]+')
        for idx, val in enumerate(reader.next()):
            header[val] = idx
        for row in reader:
            if len(row) != len(header):
                continue
            prisoner_id_sanitized = pattern.sub('',row[header['PrisonerID']])
            print "ID: %s " % prisoner_id_sanitized
            if row[header['BookEnrollDate']] == '00/00/00':
                book_date = '2000-01-01'
            else:
                book_date = time.strptime(row[header['BookEnrollDate']], "%m/%d/%y")
                book_date = datetime.fromtimestamp(time.mktime(book_date))
            print "BookEnrollDate: %s" % book_date
            
            a = Address(city=row[header['City']],
                        state=row[header['State']],
                        postal_code=row[header['ZipCode']],
                        address_1=row[header['PreAddress']],
                        address_2=row[header['Address']])
            a.save()
            p = Prisoner(name=row[header['FirstName']] +' '+
                                 row[header['LastName']],
                         prisoner_id_raw=row[header['PrisonerID']],
                         prisoner_id=prisoner_id_sanitized,
                         last_active=book_date,
                         address=a)
            p.save()
