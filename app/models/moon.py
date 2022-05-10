from sqlalchemy import ForeignKey
from app import db

class Moon(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    planet = db.relationship("Planet", backpopulates = "moons")
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"))
    

    def make_dict(self):
        return dict(
                id=self.id,
                name=self.name,
            )
    
    def replace_all_details(self, data_dict):
        self.name = data_dict["name"]
        
    # *************************
    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            name = data_dict["name"], 
            )
