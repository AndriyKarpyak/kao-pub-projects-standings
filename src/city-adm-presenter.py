# -*- coding=utf-8 -*-
import sqlite3
import xlsxwriter
from collections import OrderedDict


def read(project_ids):
    conn = sqlite3.connect('votes.db')
    c = conn.cursor()

    query = 'SELECT * FROM votes WHERE Project in %s ORDER BY Project' % str(project_ids)
    query_result = c.execute(query).fetchall()

    formatted = OrderedDict(OrderedDict())

    for record in query_result:
        number = record[0]
        votes = record[1]
        date = record[2]
        if date not in formatted:
            formatted[date] = OrderedDict()
            formatted[date][number] = votes
        else:
            formatted[date][number] = votes

    conn.close()

    return formatted


def export_xlsx(name, table):
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(name + '.xlsx')
    worksheet = workbook.add_worksheet()

    # Iterate over the data and write it out row by row.
    col = 0
    for number in table.values()[0]:
        worksheet.write(0, col + 1, number)
        col += 1

    # Iterate over the data and write it out row by row.
    row = 1
    col = 0
    for date, votes in table.iteritems():
       # if date.startswith('15-11') or date.startswith('14-11'):
        worksheet.write(row, col, date)
        for number, vote in votes.items():
            col += 1
            worksheet.write(row, col, vote)
        row += 1
        col = 0

    workbook.close()


def main():
    export_xlsx(u"Малі проекти на личакові", read((14, 136, 146, 158)))
    export_xlsx(u"Великі проекти", read((26, 36, 39, 45, 167, 215, 222)))


if __name__ == '__main__':
    main()
