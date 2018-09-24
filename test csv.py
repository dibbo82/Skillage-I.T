import csv

with open('Wood Stock.csv','r') as csv_file:
    csv_reader = csv.reader(csv_file)
    
    with open('New Wood Stock.csv','w') as new_file:
        csv_writer = csv.writer(new_file, delimiter='_')
        
        for line in csv_reader:
            csv_writer.writerow(line)
            
            
            
                
            