import mysql.connector

#create mysql q.connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="1234",
  database="lic"
)

mycursor = mydb.cursor()

#reset all tables
def reset():
  mycursor.execute("truncate keyword_appr")
  mycursor.execute("truncate main_topic")
  mycursor.execute("truncate sub_topic")
  mycursor.execute("truncate policy_name")

  print("reset complete")

#Note- you need to manually delete all neo4j nodes using cypher query - MATCH (n) DETACH DELETE n
