import datetime
file = open('Logs/1.txt', 'a')
file.write(str(datetime.date.today()) + "\n")
file = open('Logs/2.txt', 'a')
file.write(str(datetime.date.today()) + "\n")
print("Done")