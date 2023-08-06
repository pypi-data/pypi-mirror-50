#!/usr/bin/env python3
from time import sleep
from setuptools import setup
import datetime, os

setup(
    name='todo-pikkko',
    version='0.9',
    scripts=['todo']
)

os.system("set echo off")
def add():
    print("Text:", end=' ')
    task = input()
    time = str(datetime.datetime.now())
    time = time[:19]
    file = open("todo.txt", "a+")
    file.write("\n"+time+"\n"+task+"\n")
    file.close()
    os.system("clear")
    print("You saved the task with this:")
    print("Time: {}".format(time))
    print("Description: {}".format(task))
    print("Write and Press any key to continue..")
    input()
    os.system("clear")
    main()

def read():
    reader = open("todo.txt", "r")
    for line in reader.readlines():
        print(line)
    print("Write and Press any key to continue..")
    input()
    os.system("clear")
    main()

def cleartask():
    os.remove("todo.txt")
    print("Done")
    print("Write and Press any key to continue..")
    input()
    os.system("clear")
    main()

def main():
    print("Hello, what do you want?:")
    print("1. Add Task")
    print("2. Read Tasks")
    print("3. Clear Tasks")
    print("4. Exit")
    try:
        answer = int(input())

        if answer==1:
            os.system("clear")
            add()
        elif answer==2:
            os.system("clear")
            read()
        elif answer==3:
            os.system("clear")
            print("Are you sure\nall tasks will be removed!")
            print("yes/no")
            sure = input()
            if sure=="yes":
                os.system("clear")
                cleartask()
            elif sure=="no":
                os.system("clear")
                main()
            else:
                print("Wrong answer")
                sleep(2)
                os.system("clear")
                main()
        elif answer==4:
            os.system("clear")
            exit
        else:
            print("Wrong number")

    except Exception as e:
        print(e)

os.system("clear")
main()
os.system("set echo on")
