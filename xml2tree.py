import sys, os
import consts

def parse_ins(x):
    n_ins = 0
    d = x
    pos, ins = d.split('.')
    # problem about 'XC' to be solved, so far
    # those events are not considered
    try:
        n_ins = int(ins[0])
        nat_ins = ins[1:]
        return '.'.join([pos, nat_ins*n_ins])
    except ValueError:
        pass

def retro_handle(i):
    # this function should be called before checking if the mutation is either a transition or a transversion.
    u = mut_handle(i.replace('!', ''))
    # an even number of "!" means that the change is actually occurring
    if i.count('!')%2 == 0:
        n = u
    # an odd number of "!" means that there is actually a retromutation
    else:
        n = u+'!'
    # check if the mutation is a transition or a transversion
    return n

def mut_handle(i):
    #print i
    # preliminar check of deletion
    if "." in i:
        n = parse_ins(i)
        if n is None:
            pass
    elif "d" in i:
        # in new phylotree versions deletions of single nts
        # are preceded by nt but have to be removed
        if i[0].isdigit() == False:
            n = i[1:]
        else:
            n = i
    else:
        x, y = [i[0].upper(), i[-1].upper()]
        if (x in consts.PUR and y in consts.PUR) or (x in consts.PYR and y in consts.PYR):
            # transition, from "G100A" get "100"
            n = i[1:-1]
        elif (x in consts.PUR and y in consts.PYR) or (x in consts.PYR and y in consts.PUR):
    	    # transversion, from "C100A" get "100A"
    	    n = i[1:].upper()
    return n


def events_parsing(string):
    # cfr events_parsing
    n_events = []
    events = string.split(',')
    # events between brackets are discarded
    events = [i for i in events if i[0] != '(']
    for e in events:
        # note: the function "retro_handle" handles all mutation types
        if "X" in e:
            print "%s, mutation ignored." % e
            continue
        e = retro_handle(e)
        if e is None:
            continue
        n_events.append(e)
    return n_events


inhandle = sys.argv[1]



s = raw_input('\nThe first line of the file mtDNAPhylogeny.xml MUST BE a Node Id.\nNo <?xml tags> or <Node Id="mtDNAPhylogeny">, please.\nUsing a file with such lines could have unpredictable effects on tree parsing.\n\nAre you sure your file is consistent with the aforementioned rule? yes/no ')

if s == "yes":
    print "\nLet's go on then!!\n"
else:
    print "\nCheck your file and try again.\n"

a = open(inhandle, 'r')
b = open(inhandle+'.csv', 'w')
l = []
line = a.readline()
if "mtdnaphylogeny" in line.lower() or "xml" in line.lower():
    print "\nHey hey... The file is not consistent with my rules.\nARE YOU KIDDING ME?\nQuitting...\n"
    sys.exit()
while line:
    l.append(line.strip())
    line = a.readline()

# counter of indents
c = 0

for x,i in enumerate(l):
    #print c
    #print "x = ", x, "="*50
    #print i
    if i.startswith("</Node>"):
        c-=1
        #print c
        continue
    else:
        #print i
        # check node has positions and not xml closing tag
        if i.endswith('\">'):
            #print "still inside"
            #print "check this", l[x+2-1]
            if l[x-1].startswith("</Node>") == False:
                c+=1
        elif i.endswith("/>"):
            if l[x-1].endswith('\">'):
                #print "still inside"
                c+=1
            #else:
                #print "stop"
        r = i.split('"')
        h = [r[1], r[3]]
        # print h[1]
        # print events_parsing(h[1])
        try:
            events = ','.join(events_parsing(h[1]))
        except:
            sys.exit
        # put here events parsing
        # events = events_parsing(h[1])
        if c == 0:
            b.write(",".join([h[0], events])+'\n')
        else:
            b.write(",".join([","*(c-1), h[0], events])+'\n')

b.close()
