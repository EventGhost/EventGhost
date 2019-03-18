import eg
import OpenOPC
import time

opc = OpenOPC.client()
print opc.servers()
#opc.connect('Eiris.Siemens.OPC.Server.DA', 'localhost')
opc.connect('Matrikon.OPC.Simulation.1', 'localhost')
all_tags = []
all_items = []
more_tags = []
result = [0]
root_tags = opc.list()
all_tags.extend(root_tags)
    
while len(result) > 0:
    for i in range (0,len(root_tags)):
        #print str(root_tags[i])
        result = opc.list(str(root_tags[i]))
        if len(result) > 0:
            print result
            all_tags.extend(result)
    result = []

print all_tags

for j in range (0,len(all_tags)):
    items = opc.list('*.*', recursive=True)
    if len(items) > 0:
        all_items.append(items)

print all_items

opc.close()


__________________________________________________________________________________________


import eg
import OpenOPC
import time

opc = OpenOPC.client()
opc.connect('Matrikon.OPC.Simulation.1', 'localhost')
list = opc.list()
print list
for i in range(0,len(list)):
    list.extend(opc.list(str(list[i])))
print list
for j in range(0,len(list)):
    t_list = opc.list(str(list[j]))
    print t_list
print opc.list('Simulation Items.Bucket Brigade')

opc.connect('Eiris.Siemens.OPC.Server.DA', 'localhost')
list = opc.list()
print list
for i in range(0,len(list)):
    list.extend(opc.list(str(list[i])))
print list
for j in range(0,len(list)):
    t_list = opc.list(str(list[j]))
    print t_list

opc.close()


__________________________________________________________________________________________________


import eg
import OpenOPC
import time

opc = OpenOPC.client()
#opc.connect('Matrikon.OPC.Simulation.1', 'localhost')
opc.connect('Eiris.Siemens.OPC.Server.DA', 'localhost')
root_tags = opc.list()
#print root_tags
level_1_tags = []
level_2_tags = []

for i in range (0,len(root_tags)):
    result = opc.list(root_tags[i])
    #print result
    if len(result) > 0:

        for j in range (0,len(result)):
            if result[j].find('.')!=-1:
                level_1_tags.append(result[j])
            else:
                #print root_tags[i]+'.'+result[j]
                level_1_tags.append(root_tags[i]+'.'+result[j])


if len(level_1_tags) > 0:
    for i in range (0,len(level_1_tags)):
        result = opc.list(level_1_tags[i])
        if len(result) > 0:

            for j in range (0,len(result)):
                if result[j].find('.')!=-1:
                    #print result[j]
                    level_2_tags.append(result[j])
                else:
                    level_2_tags.append(root_tags[i]+'.'+result[j])

print "level_1_tags", level_1_tags
print "level_2_tags", level_2_tags

# Create lists of items
tags = level_1_tags
if len(level_2_tags) >0:
    tags = level_2_tags
    
items = []
for i in range (0,len(tags)):
    n_items = opc.list(tags[i], recursive = True)
    if len(n_items) > 0:
        items.append(n_items)
        print n_items
    else:
        items.append(tags[i])

print "items: ", items

for i in range (0,len(items)):
    print opc.properties(items[i], id=1)



opc.close()


______________________________________________________________________________________________________


import eg
import OpenOPC
import time

opc = OpenOPC.client()
my_opc = ['Matrikon.OPC.Simulation.1', 'Eiris.Siemens.OPC.Server.DA']
for k in range (0,len(my_opc)):
    opc.connect(my_opc[k])
    root_tags = opc.list()
    print "root tags", root_tags
    below_root_tags = []

    for i in range (0,len(root_tags)):
        result = opc.list(root_tags[i])
        print "result", result
        if len(result) > 0:
            for j in range (0,len(result)):
                if result[j].find('.')!=-1:
                    if root_tags[i] not in below_root_tags:
                        below_root_tags.append(root_tags[i])
                else:
                    below_root_tags.append(root_tags[i]+'.'+result[j])
    print "below_root_tags", below_root_tags
    
    # Create lists of items
    tags = below_root_tags
    tag_items = {}
    for i in range (0,len(tags)):
        t_items = opc.list(tags[i])
        tag_items[tags[i]] = t_items
    print "tag items: ", tag_items

#    print tag_items[tags[0]]
#    print "Read", opc.read(tag_items[tags[0]][0])
#    print "Prop", opc.properties(tag_items[tags[0]][0], id=1)

    for i in range (0,len(tags)):
        t_items = tag_items[tags[i]]
        print t_items
        for j in range (0,len(t_items)):
            print opc.properties(t_items[j], id=1 )
#

    opc.close()






