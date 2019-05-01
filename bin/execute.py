from pathlib import Path
import spacy
from advancedquery import map_document_structure as mds
from advancedquery import query as q

directory_in_str=""

pathlist=Path(directory_in_str).glob('**/*.txt')
path_list=[]
for path in pathlist:
    path_in_str = str(path)
    path_in_str = path_in_str.replace('C:\\Users\\Omkar\\lic\\',"",1)
    path_list.append(path_in_str)

output = mds.cal_structure(path_list)

def clean_text(text):
    text=text.replace("\n","")
    text=text.replace(":","")
    return text

tuples=[]
main=[]
sub=[]
policy_name=[]
for x in output:
    if(x[0]=="policy name"):
        temp_policy_name=x[2]
        temp_policy_name=temp_policy_name.lower()
        temp_policy_name=temp_policy_name.replace(".txt","")
        temp_policy_name=temp_policy_name.replace("lic's","")
        temp_policy_name=temp_policy_name.replace("lic’s","")
        temp_policy_name=temp_policy_name.replace("'","")
        policy_name=[0,temp_policy_name]
        print("LIC","isapolicy",policy_name)
        tuples.append([[-1,"LIC"],"isapolicy",policy_name])
    elif(x[0]=="main"):
        print(policy_name,"maintopic",x[2])
        text=clean_text(x[2])
        tuples.append([policy_name,"maintopic",[x[1],text]])
        main=[x[1],text]
    else:
        print(main,"subtopic",x[2])
        text=clean_text(x[2])
        tuples.append([main,"subtopic",[x[1],text]])

nlp = spacy.load('en_core_web_sm')
def return_lemmas(text):
    text=nlp(text)
    keywords=[]
    for token in text:
        if(not token.is_stop):
            if(token.pos_=='NOUN' or token.pos_=='VERB' or token.pos_=='ADJ'):
                keywords.append(token.lemma_)
    return keywords

for elem in tuples:
    if(elem[1]=="isapolicy"):
        q.conn.print_node(elem[0],"organization")
        q.conn.print_node(elem[2],"policyName")
        q.conn.print_rel(elem[0],"is_parent_of",elem[2],"organization","policyName")

    elif(elem[1]=="maintopic"):
        q.conn.print_node(elem[0],"policyName")
        q.conn.print_node(elem[2],"mainTopic")
        q.conn.print_rel(elem[0],"is_parent_policy_of",elem[2],"policyName","mainTopic")

    else:
        q.conn.print_node(elem[0],"mainTopic")
        q.conn.print_node(elem[2],"subTopic")
        q.conn.print_rel(elem[0],"is_a_maintopic_of",elem[2],"mainTopic","subTopic")
