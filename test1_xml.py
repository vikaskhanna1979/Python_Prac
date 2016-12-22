import xlrd

workbook = xlrd.open_workbook('country_names.xlsx')
workbook = xlrd.open_workbook('country_names.xlsx', on_demand = True)
worksheet = workbook.sheet_by_index(0)
n1 = "\n"
first_row = [] # The row where we stock the name of the column
for col in range(worksheet.ncols):
    first_row.append( worksheet.cell_value(0,col) )
# tronsform the workbook to a list of dictionnary
data =[]
elm = dict() 
for row in range(1, worksheet.nrows):
 #   for col in range(worksheet.ncols):
   # elm[worksheet.cell_value(row,0)]=worksheet.cell_value(row,1)
    if worksheet.cell_value(row,1) in elm.keys():
         elm[worksheet.cell_value(row,1)].append(worksheet.cell_value(row,0))
    else:
         elm[worksheet.cell_value(row,1)] = []
         elm[worksheet.cell_value(row,1)].append(worksheet.cell_value(row,0))
       #  elm.update({worksheet.cell_value(row,1) : worksheet.cell_value(row,0)})
# Generate enum for customer name for each country
for key in elm:
   print "typdedef customer" + key + "{"
   print " description" 
   print '"' + key + " customer names" + '"'
   print "type enumeration {"
   for customer in elm[key]:
     print "  enum " +  customer.encode("utf-8") + ";"
   print " }"
   print "}"
   print n1

# Generate grouping for country
print "grouping country {"
print "   choice country-name{" 
for key in elm:
   print  "     case " +  key + "{"
   print  "      leaf customer-" + key + " {"
   print  "      type Customer" + key + ";"   
   print "   }"
   print "  }"
   print n1
print " }"
print "}"
