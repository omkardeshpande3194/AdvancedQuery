import mysql.connector
import neo4j
import spacy
from collections import defaultdict

#create mysql connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="1234",
  database="lic"
)

mycursor = mydb.cursor()

#add entries to sql database
def put_mysql_entry(name_type,name,name_id,keywords):
    
    print()
    if(name_type=="policyName"):
        sql = "INSERT IGNORE INTO policy_name (policy_name,kg_id) VALUES ('"+name[1]+"',"+str(name_id)+")"
        print(sql)
        mycursor.execute(sql)
        print("1 record inserted, ID:", mycursor.lastrowid)
        
        for x in keywords:
            sql = "INSERT IGNORE INTO keyword_appr (Keyword,node_id,label) VALUES ('"+x+"',"+str(name_id)+",'"+name_type+"')"
            print(sql)
            mycursor.execute(sql)
            print("1 record inserted, ID:", mycursor.lastrowid)
            
        print(name_id,name_type,name)
        print(keywords)
        
    elif(name_type=="mainTopic"):
        
        sql = "INSERT IGNORE INTO main_topic (main_topic,kg_id) VALUES ('"+name[1]+"',"+str(name_id)+")"
        print(sql)
        mycursor.execute(sql)
        print("1 record inserted, ID:", mycursor.lastrowid)
        
        for x in keywords:
            sql = "INSERT IGNORE INTO keyword_appr (Keyword,node_id,label) VALUES ('"+x+"',"+str(name_id)+",'"+name_type+"')"
            print(sql)
            mycursor.execute(sql)
            print("1 record inserted, ID:", mycursor.lastrowid)
        
        print(name_id,name_type,name)
        print(keywords)
        
    elif(name_type=="subTopic"):

        sql = "INSERT IGNORE INTO sub_topic (sub_topic,kg_id) VALUES ('"+name[1]+"',"+str(name_id)+")"
        print(sql)
        mycursor.execute(sql)
        print("1 record inserted, ID:", mycursor.lastrowid)
        
        for x in keywords:
            sql = "INSERT IGNORE INTO keyword_appr (Keyword,node_id,label) VALUES ('"+x+"',"+str(name_id)+",'"+name_type+"')"
            print(sql)
            mycursor.execute(sql)
            print("1 record inserted, ID:", mycursor.lastrowid)
            
        print(name_id,name_type,name)
        print(keywords)
    
    else:
        print("error")


#create neo4j connection
from neo4j import GraphDatabase

#Neo4j query functions
class connectionObj(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def print_node(self, name,of_type):
        keywords=return_lemmas(name[1])
        with self._driver.session() as session:
            res = session.write_transaction(self._create_node, name,of_type,keywords)
            put_mysql_entry(of_type,name,res,keywords)
            
    def print_rel(self,en1,rel,en2,of_type1,of_type2):
        with self._driver.session() as session:
            res = session.write_transaction(self._create_rel,en1,rel,en2,of_type1,of_type2)
            
    def get_nodes(self):
        with self._driver.session() as session:
            return session.read_transaction(self.get_all_nodes)
        
    def match_nodes_by_id(self,ids):
        with self._driver.session() as session:
            return session.read_transaction(self.get_matched_nodes_by_id,ids)
        
    def get_ontology(self,ids_dict):
        with self._driver.session() as session:
            return session.read_transaction(self.get_matched_ontology,ids_dict)
        
    @staticmethod
    def _create_node(tx, name,of_type,keywords):
    
        keywords_str=""
        for keyword in keywords:
            keywords_str=keywords_str+","+keyword
        keywords_str=keywords_str[1:]
        
        result = tx.run("MERGE (a:"+of_type+" { name : '"+name[1]+"',seriality :'"+str(name[0])+"',keywords :'"+keywords_str+"' })"
                        "RETURN "+ "id(a)")
        
        return result.single()[0]
    
    @staticmethod
    def _create_rel(tx,en1,rel,en2,of_type1,of_type2):
        result = tx.run("MATCH (a:"+of_type1+"),(b:"+of_type2+")"
                        "WHERE a.name = '"+en1[1]+"' AND b.name = '"+en2[1]+"'"
                        "MERGE (a)-[r:"+rel+"]->(b)"
                        "RETURN type(r)")
        return result
    
    @staticmethod
    def get_all_nodes(tx):
        result= list(tx.run("MATCH (n)"
                           "RETURN n"))
        return result
    
    @staticmethod
    def get_matched_nodes_by_id(tx,ids):
        
        return list(tx.run("MATCH (n)"
                           "WHERE ID(n) IN "+ids+""
                           "RETURN n"))

    
    @staticmethod
    def get_matched_ontology(tx,ids_dict):
        result = defaultdict(list)
        
        for x in ids_dict:
            if(ids_dict[x]=='subTopic'):
                res= list(tx.run("OPTIONAL MATCH (a:subTopic)-[x]-(b:mainTopic)-[y]-(c:policyName)"
                                 "WHERE id(a)="+str(x)+" "
                                 "RETURN a,b,c"))
                result[x].append(res)              
            elif(ids_dict[x]=='mainTopic'):
                res= list(tx.run("MATCH (b:mainTopic)-[y]-(c:policyName) "
                                 "WHERE id(b)="+str(x)+" "
                                 "WITH b,c "
                                 "OPTIONAL MATCH (a:subTopic)-[x]-(b:mainTopic)-[y]-(c:policyName) "
                                 "WHERE a IS NULL "
                                 "RETURN a,b,c"))
                result[x].append(res)
            else:
                res=list(tx.run("MATCH (a)"
                                 "WHERE id(a)="+str(x)+" "
                                 "RETURN a"))
                result[x].append(res)
        return result

conn=connectionObj("bolt://localhost:11004","neo4j","1234")

#get keywords of input
nlp = spacy.load('en_core_web_sm')
def return_lemmas(text):
    text=nlp(text)
    keywords=[]
    for token in text:
        if(not token.is_stop):
            if(token.pos_=='NOUN' or token.pos_=='VERB' or token.pos_=='ADJ'):
                keywords.append(token.lemma_)
    return keywords

#test function
def test_query():
    exit=1
    while(exit==1):
        print("1 - Query 2 - Exit ")
        exit=input()
        exit=int(exit)

        if(exit!=1):
            print("successfully exited")
            break
            
        print("Enter text to find relevant nodes")
        txt=input()

        keywords=return_lemmas(txt)

        find_query="Keyword='"+keywords[0]+"'"
        for x in keywords[1:]:
            find_query=find_query+" OR Keyword='"+x+"'"

        mycursor.execute("SELECT * FROM keyword_appr WHERE "+find_query)

        res_keywords = defaultdict(list)
        topic_list={}

        for x in mycursor:
            print(x)
            res_keywords[x[2]].append(x[1])  
            if x[2] not in topic_list:
                topic_list[x[2]]=x[3]

        final_res_keywords={}

        for x in res_keywords:
            final_res_keywords[x]={}
            temp=res_keywords[x]
            occured=[]
            for y in temp:
                if y not in occured:
                    final_res_keywords[x][y]=temp.count(y)
                    occured.append(y)

        for x in final_res_keywords:
            final_res_keywords[x]['len']=len(final_res_keywords[x])
            final_res_keywords[x]['label']=topic_list[x]

        sorted_res=sorted(final_res_keywords, key=lambda x: (final_res_keywords[x]['len']),reverse=True)

        sorted_dict={}
        for x in sorted_res[:10]:
            sorted_dict[x]=final_res_keywords[x]['label']

        ontology=conn.get_ontology(sorted_dict)

        policies=[]
        main_topics=[]
        sub_topics=[]
        for x in ontology:

            y=len(ontology[x][0])
            print("*****************           "+str(x)+"      ***********************")

            for i in range(0,y):
                if(len(ontology[x][0][i])==3):
                    if 'a' in ontology[x][0][i]:
                        try:
                            print(ontology[x][0][i]['a'])
                            sub_topics.append([ontology[x][0][i]['a']['name'],ontology[x][0][i]['b']['name']])
                        except:
                            print("no a")
                    try:
                        print(ontology[x][0][i]['b'])
                        main_topics.append([ontology[x][0][i]['b']['name'],ontology[x][0][i]['c']['name']])
                    except:
                        print("no b")
                    try:
                        print(ontology[x][0][i]['c'])
                        policies.append(ontology[x][0][i]['c']['name'])
                    except:
                        print("no c")
                    print("===============================")
                else:
                    try:
                        print(ontology[x][0][i]['a'])
                        policies.append(ontology[x][0][i]['a']['name'])
                    except:
                        print("no c")
                    print("===============================")
                print()

        ranked_main_topics = {}

        for x in main_topics:
            if x[0] not in ranked_main_topics:
                ranked_main_topics[x[0]]={}
                ranked_main_topics[x[0]]['count']=1
                ranked_main_topics[x[0]][x[1]]=1
                
            else:
                if x[1] not in ranked_main_topics[x[0]]:
                    ranked_main_topics[x[0]][x[1]]=1
                else:
                    ranked_main_topics[x[0]][x[1]]=ranked_main_topics[x[0]][x[1]]+1
                ranked_main_topics[x[0]]['count']=ranked_main_topics[x[0]]['count']+1

        ranked_main_topics=sorted(ranked_main_topics, key=lambda x: (ranked_main_topics[x]['count']),reverse=True)

        ranked_policies={}
        for x in policies:
            if x not in ranked_policies:
                ranked_policies[x]=1
            else:
                ranked_policies[x]=ranked_policies[x]+1

        ranked_main_topic={}
        for x in main_topics:
            if x[0] not in ranked_policies:
                ranked_main_topic[x[0]]=1
            else:
                ranked_main_topic[x[0]]=ranked_main_topic[x[0]]+1