import CSV

#Reg reader/writer
#new_csvReader printed would just show an obj in mem
new_csvReader = csv.reader(COVID19DeathsByWeek_AgeSex.text)
"""#Skips over first element
next(new_csvReader)"""
#w indicates writing new file; a could be used to just append to file
with open('COVID19DeathsByWeek_AgeSex.csv', 'w') as COVID19DeathsByWeek_AgeSex_write:
    """#Does nothing but create file
    pass"""
    COVID19DeathsByWeek_AgeSex_write.write(COVID19DeathsByWeek_AgeSex.text)
"""for element in new_csvReader:
    print(element)"""

with open('COVID19DeathsByWeek_AgeSex.csv', 'r') as COVID19DeathsByWeek_AgeSex_read:
    #\t for tab delimiter
    csvReader = csv.reader(COVID19DeathsByWeek_AgeSex_read, delimiter=',')
    for element in csvReader:
        print(element)