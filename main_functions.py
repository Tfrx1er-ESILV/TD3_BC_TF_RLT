import csv , os
os.system("clear")

#Lecture du fichier log_id
def import_log():
    log = []
    with open('log_id.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            log.append(row[0])
            log.append(row[1])
    
    return [log[2],log[3]]   

"ID","Password"
"1032","hiuzhciuv"