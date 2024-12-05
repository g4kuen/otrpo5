#models.py

from neomodel import StructuredNode, StringProperty, RelationshipTo
from neomodel import config

from dotenv import load_dotenv
import os

load_dotenv()

config.DATABASE_URL = os.getenv("NEO4J_URL")
config.USERNAME = os.getenv("NEO4J_USER")
config.PASSWORD = os.getenv("NEO4J_PASSWORD")


class User(StructuredNode):
    uid = StringProperty(unique_index=True)
    label = StringProperty()
    name = StringProperty()
    about = StringProperty()
    home_town = StringProperty()
    photo_max = StringProperty()
    screen_name = StringProperty()
    sex = StringProperty()
    style = StringProperty()
    visualisation = StringProperty()

    follows = RelationshipTo('User', 'FOLLOW')
    subscribes = RelationshipTo('User', 'SUBSCRIBE')
