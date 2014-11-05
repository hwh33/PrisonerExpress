from PrisonerExpress.models import Prisoner, Address
import re, string
import csv

def read_file(fname):
    with open(fname, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        header = {}
        pattern = re.compile('[\W_]+')
        for idx, val in enumerate(reader.next()):
            header[val] = idx
        for row in reader:

            prisoner_id_sanitized = pattern.sub('',row[header['PrisonerID']])
            a = Address(city=row[header['City']],
                        state=row[header['State']],
                        postal_code=row[header['ZipCode']],
                        address_1=row[header['PreAddress']],
                        address_2=row[header['Address']])
            a.save()
            p = Prisoner(name=row[header['FirstName'] +
                                 header['LastName']],
                         prisoner_id_raw=row[header['PrisonerID']],
                         prisoner_id=prisoner_id_sanitized,
                         address=a)
            p.save()