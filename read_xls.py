from xlrd import open_workbook
from sys import argv
script,excel_filename = argv
output_file = open(excel_filename + ".yang", 'w')
wb = open_workbook(excel_filename)
values = []
n1 = "\n"


for s in wb.sheets():
    print 'Sheet:',s.name
    for row in range(1, s.nrows):
        col_names = s.row(0)
        countries = []
        customers = []
        for name, col in zip(col_names, range(s.ncols)):
         	value  = (s.cell(row,col).value)
            	try : value = str(int(value))
            	except : pass
                if name.value == "Countries":
            	   countries.append((value))
                   values.append(countries)
                else:
                   customers.append((value))
                   values.append(customers) 
                  
print customers
print countries 
print values
