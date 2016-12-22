from sys import argv

script,filename = argv
global classname
global attrtype
global attribute_counter
input_file = open(filename,'r')
output_file = open(filename + ".yang" , 'w')
cl = "Class="

n1 = "\n"
for line in input_file.readlines():
    if cl in line :
    	classname = line.split("=")[1].strip()
        attribute_counter = 1
    else :
  	if line.isspace() == False :
                 # parse attribute name and value
		attrname = line.split(":")[0].strip()
                attrvalue = unicode(line.split(":")[1].strip(), 'utf-8')
                # attribute type defaults to string
                attrtype = "string"
                 # check the type of attribute string/uint32/boolean 
                if attrvalue.isnumeric() == True :
                        attrtype = "int32" 
			print "attr " + attrname + "has numeric value: " + attrvalue
                else : 
			if attrvalue == "true" or attrvalue == "false":
                                attrtype = "boolean"
                        	print "attr " + attrname + "is boolean value: " + attrvalue 

   		output_file.write( "leaf" + " " + classname + "-" +attrname  + "_" + str(attribute_counter)+ "{" +n1 )
    		output_file.write("	type " + attrtype +";" +n1 )
		output_file.write( "}" +n1)                                        
 		attribute_counter = attribute_counter + 1               
                 
input_file.close()
output_file.close()
