import mysql.connector
import datetime

class InsertDB:
    
    mydb_name = "goodonyou"

    def insert_document(self, documents, table_name):
        print(documents)

        # ************** DIGITAL SERVER ***************#
        mydb = mysql.connector.connect(
            user = "root",
            password = "",
            host = "localhost"
        )

        mycursor = mydb.cursor()

        mycursor.execute("CREATE DATABASE IF NOT EXISTS " + self.mydb_name + " CHARACTER SET utf8 COLLATE utf8_general_ci")

        # ********** DIGITAL OCEAN SERVER ***********#
        mydb = mysql.connector.connect(
            user = "root",
            password = "",
            host = "localhost",
            database = self.mydb_name
        )

        documents = documents[0]
        print(documents)

        mycursor = mydb.cursor()

        stmt = "SHOW TABLES LIKE '{}'".format(table_name)
        mycursor.execute(stmt)
        result = mycursor.fetchone()

        if not result:
            sql = "CREATE TABLE {} (id INT(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY, Brand VARCHAR(50), Title Text, Planet VARCHAR(20), People VARCHAR(20), Animals VARCHAR(10), Overall_Rating VARCHAR(50), Description Text, Identifier VARCHAR(100), CreatedTime VARCHAR(30), UpdatedTime VARCHAR(30), INDEX (Identifier))".format(table_name)

            mycursor.execute(sql)
            mydb.commit()


        sql = "SELECT Identifier FROM {0} WHERE Identifier='{1}'".format(table_name, documents[7])
        mycursor.execute(sql)
        identifier_result = mycursor.fetchone()

        if not identifier_result:
            print("MYSQL ADD")
            insert_sql = """INSERT INTO {} (Brand, Title, Planet, People, Animals, Overall_Rating, Description, Identifier, CreatedTime, UpdatedTime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""".format(table_name)

            mycursor.execute(insert_sql, documents)
            mydb.commit()

        else:
            update_sql = 'UPDATE {0} SET Brand="{1}", Title="{2}", Planet="{3}", People="{4}", Animals="{5}", Overall_Rating="{6}", Description="{7}", UpdatedTime="{8}" WHERE Identifier="{9}"'.format(table_name, documents[0], documents[1], documents[2], documents[3], documents[4], documents[5], documents[6], datetime.datetime.now(), documents[7])
            
            print("Updated")
            mycursor.execute(update_sql)
        
            mydb.commit()
        print("==================> Now time:", datetime.datetime.now())