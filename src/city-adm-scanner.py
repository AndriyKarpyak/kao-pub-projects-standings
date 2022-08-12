#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import codecs

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from lxml import html
from lxml.etree import tostring
from datetime import datetime
import requests
import sqlite3

from ProjectBean import Project


def store(now, projects):
    c = sqlite3.connect('votes.db')
    c.text_factory = str

    # c.execute('''CREATE TABLE "projects" (
    #             "Number"	INTEGER NOT NULL UNIQUE,
    #             "Name"	TEXT NOT NULL,
    #             "Budget"	INTEGER NOT NULL,
    #             "Size"	TEXT NOT NULL,
    #             "Category"	TEXT NOT NULL,
    #             PRIMARY KEY("Number")
    #         )''')

    # c.execute('''CREATE TABLE "votes" (
    #             "Project"	INTEGER NOT NULL,
    #             "Votes"	INTEGER NOT NULL,
    #             "Date"	TEXT NOT NULL,
    #             FOREIGN KEY("Project") REFERENCES "projects"("Number")
    #         )''')

    for number, project in projects:
        c.execute('INSERT OR IGNORE INTO projects VALUES (?,?,?,?,?)',
                  (
                      project.parsed_number(),
                      project._name,
                      project._budget,
                      project._size,
                      project._type)
                  )

    for number, project in projects:
        c.execute('INSERT INTO votes VALUES (?,?,?)',
                  (
                      project.parsed_number(),
                      project._votes,
                      now)
                  )
    c.commit()
    c.close()


def scan_single(size, category, count, url):
    projects = dict()

    while True:
        page = requests.get(url)

        tree = html.fromstring(page.content.decode('utf-8'))

        cards = tree.xpath('//*[@id="content"]/div/div/section/ul/*/article')

        for card in cards:
            card_html = html.fromstring(tostring(card).decode('utf-8'))

            number = card_html.xpath('//article/div/span[1]/text()')[0].encode('utf-8')
            votes = int(card_html.xpath('//article/div/div[1]/ul/li[4]/strong/text()')[0].rstrip().strip().replace(" ", "").encode('utf-8'))
            name = card_html.xpath('//article/div/h1/a/text()')[0].rstrip().strip().encode('utf-8')
            budget = card_html.xpath('//article/div/div[1]/ul/li[3]/strong/text()')[0].encode('utf-8')

            project = Project(number, name, budget, votes, size, category)
            projects[number] = project

        if projects.__len__() == count:
            break

    return projects


def scan():
    print ''
    now = datetime.now().strftime("%d-%m %H:%M")
    print sys.getdefaultencoding()
    print sys.stdout.encoding
    print now + ' починаю читати дані опитування.'.decode('utf-8').encode(sys.stdout.encoding)

    # ------------------------------------------------------------------------------------------------------------------
    result = scan_single("small", "gen", 8,
                         'https://lviv.pb.org.ua/projects?'
                         'status=voting&project_type=460&category%5B%5D=15&districts%5B%5D=3&budget=110000%3A3000000')
    print ""
    print "Малі не освітні проекти на личакові. За " + str(result.__len__()) + " проектів проголосувало " + str(sum(x._votes for x in result.values()))
    index = 1
    for number, project in sorted(result.items(), key=lambda item: item[1]._votes, reverse=True):
        if "136" in project._number:
            print "> " + str(project)
        else:
            print "  " + str(project)
        if index == 3:
            print "-----------------------------"
        index = index + 1

    # ------------------------------------------------------------------------------------------------------------------
    result = scan_single("large", "gen", 16,
                         'https://lviv.pb.org.ua/projects?'
                         'status=voting&project_type=461&category%5B%5D=15&budget=110000%3A3000000')
    print ""
    print "Великі не освітні проекти. За " + str(result.__len__()) + " проектів проголосувало " + str(sum(x._votes for x in result.values()))
    index = 1
    for number, project in sorted(result.items(), key=lambda item: item[1]._votes, reverse=True):
        if "45" in project._number:
            print "> " + str(project)
        else:
            print "  " + str(project)
        if index == 3:
            print "-----------------------------"
        index = index + 1

    # ------------------------------------------------------------------------------------------------------------------
    result = scan_single("large", "all", 8,
                         'https://lviv.pb.org.ua/projects?'
                         'status=voting&project_type=461&districts%5B%5D=3&budget=110000%3A3000000')
    print ""
    print "Великі проекти на личакові. За " + str(result.__len__()) + " проектів проголосувало " + str(sum(x._votes for x in result.values()))
    for number, project in sorted(result.items(), key=lambda item: item[1]._votes, reverse=True):
        if "45" in project._number:
            print "> " + str(project)
        else:
            print "  " + str(project)

    # ------------------------------------------------------------------------------------------------------------------
    result = scan_single("small", "all", 18,
                         'https://lviv.pb.org.ua/projects?'
                         'status=voting&project_type=460&districts%5B%5D=3&budget=110000%3A3000000')
    print ""
    print "Малі проекти на личакові. За " + str(result.__len__()) + " проектів проголосувало " + str(sum(x._votes for x in result.values()))
    for number, project in sorted(result.items(), key=lambda item: item[1]._votes, reverse=True):
        if "136" in project._number:
            print "> " + str(project)
        else:
            print "  " + str(project)

    # ------------------------------------------------------------------------------------------------------------------
    result = scan_single("small", "ed", 10,
                         'https://lviv.pb.org.ua/projects?'
                         'status=voting&project_type=460&category%5B%5D=9&districts%5B%5D=3&budget=110000%3A3000000')
    print ""
    print "Малі освітні проекти на личакові. За " + str(result.__len__()) + " проектів проголосувало " + str(sum(x._votes for x in result.values()))
    index = 1
    for number, project in sorted(result.items(), key=lambda item: item[1]._votes, reverse=True):
        print "  " + str(project)
        if index == 4:
            print "-----------------------------"
        index = index + 1

    # ------------------------------------------------------------------------------------------------------------------
    result = scan_single("large", "ed", 25,
                         'https://lviv.pb.org.ua/projects?'
                         'status=voting&project_type=461&category%5B%5D=9&budget=110000%3A3000000')
    print ""
    print "Великі освітні проекти. За " + str(result.__len__()) + " проектів проголосувало " + str(sum(x._votes for x in result.values()))
    index = 1
    for number, project in sorted(result.items(), key=lambda item: item[1]._votes, reverse=True):
        print "  " + str(project)
        if index == 4:
            print "-----------------------------"
        index = index + 1


def silent_scan():
    print u''
    now = datetime.now().strftime("%d-%m %H:%M")
    print now + " починаю читати дані опитування"

    # ------------------------------------------------------------------------------------------------------------------
    result = scan_single("small", "gen", 8,
                         'https://lviv.pb.org.ua/projects?'
                         'status=voting&project_type=460&category%5B%5D=15&districts%5B%5D=3&budget=110000%3A3000000')
    store(now, result.items())

    # ------------------------------------------------------------------------------------------------------------------
    result = scan_single("large", "gen", 16,
                         'https://lviv.pb.org.ua/projects?'
                         'status=voting&project_type=461&category%5B%5D=15&budget=110000%3A3000000')
    store(now, result.items())

    # ------------------------------------------------------------------------------------------------------------------
    result = scan_single("small", "ed", 10,
                         'https://lviv.pb.org.ua/projects?'
                         'status=voting&project_type=460&category%5B%5D=9&districts%5B%5D=3&budget=110000%3A3000000')
    store(now, result.items())

    # ------------------------------------------------------------------------------------------------------------------
    result = scan_single("large", "ed", 25,
                         'https://lviv.pb.org.ua/projects?'
                         'status=voting&project_type=461&category%5B%5D=9&budget=110000%3A3000000')
    store(now, result.items())

    print now + " завершено читати дані опитування"


def main(args):

    now = datetime.now().strftime("%d-%m %H:%M")
    print now + " стартую сканер."

    scan()

    if 'view' not in args:
        print ""
        print "Стартую треккер."
        silent_scan()

        scheduler = BlockingScheduler()
        scheduler.add_job(silent_scan, IntervalTrigger(hours=1))
        scheduler.start()


if __name__ == '__main__':
    main(sys.argv)
