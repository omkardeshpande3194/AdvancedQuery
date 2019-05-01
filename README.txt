==============
ADVANCED QUERY
==============

Advanced query provides a automated solution to map document structure and store document structure to Neo4j 
databse and their entries to MySQL database. It also provides a test funtion to get all relevant nodes for 
any text input. 
often looks like this::

    #!/usr/bin/env python

    from advancedquery import map_document_structure
    from advancedquery import query

    query.test()

(Note the double-colon and 4-space indent formatting above.)

Paragraphs are separated by blank lines. *Italics*, **bold**,
and ``monospace`` look like this.


A Section
=========

*map_document_structure : to map document structure of all files in the current working directory. It stores 
mapped structure in variable output.

*query : it manages connections to neo4j and mysql databses and allows to query both databases.

*reset : it allows to reset mysql database tables.

GENERAL FLOW

1 - map document structure and get output in form of tuples.

2 - store structural relations in noe4j and mysql databases.

3 - Use this information to get relevant nodes.

=============
INITIAL SETUP
=============

- python 3
- Neo4j
    create a neo4j graph and replace connection strings with current connection credentials.
- MySQL
    create mysql database and replace connection strings with current connection credentials.
    
    create tables as follows
    
    -keyword_appr
        idkeyword_appr	int(11)	NO	PRI		auto_increment
        Keyword	varchar(45)	YES	UNI		
        node_id	varchar(45)	YES	UNI		
        label	varchar(45)	YES			
    
    -policy_name
        idpolicy_name	int(11)	NO	PRI		auto_increment
        policy_name	varchar(45)	NO			
        kg_id	int(11)	NO			

    -main_topic
        idmain_topic	int(11)	NO	PRI		auto_increment
        main_topic	varchar(45)	NO			
        kg_id	int(11)	NO			

    -sub_topic
        idsub_topic	int(11)	NO	PRI		auto_increment
        sub_topic	varchar(45)	NO			
        kg_id	int(11)	NO			