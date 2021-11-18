# coding=utf-8
import csv
import time
from datetime import datetime

name_file = "small.csv"
with open(name_file) as csv_file:
    # read csv file information
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    line_count_country = {}
    next(csv_reader)
    rows = []
    dates = []
    countries = []
    for row in csv_reader:
        rows.append(row)
        dates.append(datetime.strptime(
            row[7], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d'))
        countries.append(row[8])

    dates = set(dates)
    countries = set(countries)
    date_country_buffers = {}
    # filters information by delivery_datetime
    for date in dates:
        for row in rows:
            if str(row[7]).startswith(date):
                # filters information by destination_country_code
                for country in countries:
                    if row[8] == country:
                        if str(str(date).replace('-', '') + '_' + country) not in date_country_buffers:
                            date_country_buffers[str(
                                str(date).replace('-', '') + '_' + country)] = [row]
                        else:
                            date_country_buffers[str(date).replace('-', '') +
                                                 '_' + country].append(row)

    for date_country, value in date_country_buffers.items():
        writable_data = []
        # define the header
        header = ['producer_id', 'producer_name',
                  'product_unit', 'quantity', 'specifications_id', 'delivery_datetime', 'destination_country_code']
        for id, val in enumerate(value):
            writable_data.append(val)
            if len(writable_data) <= 10000:
                # Write to files after filtering
                with open(date_country + '.csv', "wt") as c:
                    writer = csv.writer(c)
                    writer.writerow(header)
                    writer.writerows(writable_data)
                writable_data = []
