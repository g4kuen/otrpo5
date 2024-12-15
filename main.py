#main.py

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from neo4j import GraphDatabase

load_dotenv()

app = FastAPI()

NEO4J_URL = os.getenv("NEO4J_URL")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

uri = NEO4J_URL
driver = GraphDatabase.driver(uri, auth=(NEO4J_USER, NEO4J_PASSWORD))


def run_query(query, parameters=None):
    with driver.session() as session:
        result = session.run(query, parameters)
        return [record.data() for record in result]

@app.get("/nodes")
async def get_nodes():
    query = "MATCH (n:User) RETURN n.id AS id, n.name AS name"
    users = run_query(query)
    return users

@app.get("/node/{id}")
async def get_node_and_relationships(id: int):
    query = "MATCH (u:User {id: toInteger($id)}) OPTIONAL MATCH (u)-[:FOLLOW]->(f:User) OPTIONAL MATCH (u)-[:SUBSCRIBE]->(s:User) RETURN u.id AS id,  collect(f.id) AS follows,  collect(s.id) AS subscribes "


    print(query)
    user_data = run_query(query, {"id": id})
    if not user_data:
        raise HTTPException(status_code=404, detail="Node not found")

    user = user_data[0]
    return {
        "id": user["id"],
        "follows": user["follows"],
        "subscribes": user["subscribes"]
    }
@app.post("/node")
async def create_node_and_relationships(node_data: dict = None):
    if not node_data:
        raise HTTPException(status_code=400, detail="No node data provided")

    query = """
    CREATE (u:User {id: toInteger($id), name: $name, 
                     about: $about, home_town: $home_town, photo_max: $photo_max, 
                     screen_name: $screen_name, sex: $sex, style: $style, visualisation: $visualisation})
    RETURN u
    """
    run_query(query, node_data)

    if "follows" in node_data:
        for follow_id in node_data["follows"]:
            query = "MATCH (u:User {id: $id}), (f:User {id: $follow_id}) CREATE (u)-[:FOLLOWS]->(f)"
            run_query(query, {"id": node_data["id"], "follow_id": follow_id})

    if "subscribes" in node_data:
        for subscribe_id in node_data["subscribes"]:
            query = "MATCH (u:User {id: $id}), (s:User {id: $subscribe_id}) CREATE (u)-[:SUBSCRIBES]->(s)"
            run_query(query, {"id": node_data["id"], "subscribe_id": subscribe_id})

    return {"message": "Node and relationships created successfully", "node_id": node_data["id"]}

@app.delete("/node/{node_id}")
async def delete_node_and_relationships(node_id: int):
    query = """
    MATCH (u:User {id: $node_id})-[r]->()
    DELETE r, u
    """
    run_query(query, {"node_id": node_id})

    return {"message": f"Node {node_id} and its relationships deleted successfully"}
