#TEST_connect.py
from neo4j import GraphDatabase

uri = "neo4j+ssc://6f37bfb2.databases.neo4j.io"
user = "neo4j"
password = "3GIHXqOvXnL6lQb6dlIR0LKCuxsoIKyc56ARLYsjB-4"

def connect_to_neo4j(uri, user, password):
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        with driver.session() as session:
            print("Привет, подключение прошло успешно!")
    except Exception as e:
        print(f"Ошибка при подключении: {e}")
    finally:
        driver.close()

connect_to_neo4j(uri, user, password)
