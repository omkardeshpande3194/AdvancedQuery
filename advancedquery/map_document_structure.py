from queue import Empty, Full
from collections import defaultdict
import queue
import itertools
import string
import re

nums=list(range(1,100))
nums_str=[]
for x in nums:
    nums_str.append(str(x))
alphas=list(string.ascii_lowercase)

#debugg
step=0

main_list=[]
level0=queue.Queue(maxsize=30)
level1=queue.Queue(maxsize=30)
level2=queue.Queue(maxsize=30)
first=1
level=0
level0_last_elem=0
level1_last_elem=0
level2_last_elem=0
last_of_type=["NUM","",""]

def queue_get_all(q):
    items = []
    maxItemsToRetreive = 10
    for numOfItemsRetrieved in range(0, maxItemsToRetreive):
        try:
            if numOfItemsRetrieved == maxItemsToRetreive:
                break
            items.append(q.get_nowait())
        except Empty:
            break
    return items

def check_seq(elem,of_type):
    global level0_last_elem
    global level1_last_elem
    global level2_last_elem
    return 1

def add_to_main_list():
    global level

def add_to_queue(elem,of_type):
    
    global main_list
    global level
    global level0
    global level1
    global level2
    global last_of_type
    
    if(of_type=="final"):
        main_list.append(queue_get_all(level0))
        return
    
    #if type is same
    if(last_of_type[level]==of_type):
        level=level

    #type not same but similar to previous level
    elif(last_of_type[level-1]==of_type):
        level=level-1
        main_list.append(queue_get_all(level0))
        main_list[len(main_list)-1].append(list(["sub-level"]+queue_get_all(level1)))
        change=1
    
    #type not same also not similar to previous level
    else:
        level=level+1
    
    #level0
    if(level==0):
        if(of_type=="NUM"):
            level0.put(elem)
            level0_last_elem=elem[1]
            last_of_type[0]="NUM"

        elif(of_type=="ALPHA"):
            level0.put(elem)
            level0_last_elem=elem[1]
            last_of_type[0]="ALPHA"

        else:
            print("Type not found")
    
    #level1
    elif(level==1):
        if(of_type=="NUM"):
            level1.put(elem)
            leve1_last_elem=elem[1]
            last_of_type[1]="NUM"

        elif(of_type=="ALPHA"):
            level1.put(elem)
            leve1_last_elem=elem[1]
            last_of_type[1]="ALPHA"
            
        else:
            print("Type not found")
    
    #level2
    elif(level==2):
        if(of_type=="NUM"):
            level2.put(elem)
            leve2_last_elem=elem[1]
            last_of_type[2]="NUM"

        elif(of_type=="ALPHA"):
            level2.put(elem)
            leve1_last_elem=elem[1]
            last_of_type[2]="ALPHA"

        else:
            print("Type not found")
            
    #level exceeded
    else: 
        print("level error")

def create_topology(input):
    global first
    global level
    global level0_last_elem
    global level1_last_elem
    
    x=next(input, None)
    if(x):
        if(first==1):
            level0=queue.Queue(maxsize=20)
            level0.put(x[1])
            last_elem=x[1]
            first=0
            
        if(x[1] in nums_str):
            type="NUM"
            add_to_queue(x,type)
            
        if(x[1] in alphas):
            type="ALPHA"
            add_to_queue(x,type)
            
        create_topology(input)
    else:
        add_to_queue(x,"final")
        return

def cal_structure(paths):
    
    output=[]
    
    for path in paths:
                
        global main_topics
        global doc_structure
        global main_list
        global nums_str
        global alphas
        global level0
        global level1
        global level2
        global first
        global level
        global level0_last_elem
        global level1_last_elem
        global level2_last_elem
        global last_of_type
        
        main_topics=[]
        doc_structure=[]
        main_list=[]

        level0=queue.Queue(maxsize=30)
        level1=queue.Queue(maxsize=30)
        level2=queue.Queue(maxsize=30)
        first=1
        level=0
        level0_last_elem=0
        level1_last_elem=0
        level2_last_elem=0
        last_of_type=["NUM","",""]
        
        text = open(path,encoding='utf-8').read()
        text=text.lower()
        main_topics_re=re.compile(r'([\n\r])(\w\w?\w?\w?)([):.])')

        
        for match in re.finditer(main_topics_re, text):
            topic = []
            if match.group(1):
                topic.append(match.group(1))
            else:
                topic.append("None")
            if match.group(2):
                topic.append(match.group(2))
            else:
                topic.append("None")
            if match.group(3):
                topic.append(match.group(3))
            else:
                topic.append("None")
            topic.append(match.span())
            main_topics.append(topic)
        
        
        if not main_topics:
            print(text)
            continue
        
        
        for i in range(0,len(main_topics)-1):
            start=main_topics[i][3][1]
            end=main_topics[i+1][3][0]
            main_topics[i].append(text[start:end])

        main_topics[i+1].append(text[main_topics[i+1][3][1]:])
        nums=list(range(1,100))

        for x in nums:
            nums_str.append(str(x))
        
        input=iter(main_topics)
        create_topology(input)
        
        
        for x in main_list:
            for y in x:
                doc_structure.append(y)
        
        output.append(["policy name",[],path])
        
        sub_topics_re=re.compile(r'\s?\S*\s?\S*\s?\S*\s?[(]?\S*\s?\S*\s?\S*\s?\S*[)]?\s?[\n:]')
        sub_topics_re1=re.compile(r'[\n:,.;-][\s]')
        
        for x in doc_structure:
            if(x[0]=='\n'):
                try:                    
                    found=False
                    for match in re.finditer(sub_topics_re1, x[4]):
                        temp=match.span()
                        print(str(x[1])+" : "+x[4][:temp[1]])
                        output.append(["main",x[1],x[4][:temp[1]]])
                        found=True
                        break

                    if(not found):
                        print(str(x[1])," : ",x[4])
                        output.append(["main",x[1],x[4]])
                except:
                    print("\nSOME ERROR OCCURED in X\n",x)

            else:
                for y in x:
                    
                    if(y[1]=="u"):
                        print()
                    else:
                        try:
                            found=False
                            for match in re.finditer(sub_topics_re1, y[4]):
                                temp=match.span()
                                print("----------"+str(y[1])+" : "+y[4][:temp[1]])
                                output.append(["sublevel",y[1],y[4][:temp[1]]])
                                found=True
                                break

                            if(not found):
                                print("----------",str(y[1])," : ",y[4])
                                output.append(["sublevel",y[1],y[4]])
                            
                        except:
                            print("\nSOME ERROR OCCURED in Y\n",y)
        
    return output