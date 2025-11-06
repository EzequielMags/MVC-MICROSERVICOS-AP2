from models import db 
from sqlalchemy import Column, Integer, String, ForeignKey, VARCHAR, DATE, Float, Boolean
from sqlalchemy.orm import relationship 
from datetime import date

class Reservas(db.Model):
    __tablename__ = "reservas"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    num_sala = Column(Integer, nullable=False)
    lab = Column(Boolean, nullable=False)
    data = Column(DATE, nullable=False)
    # referência a entidade externa (Gerenciamento) sem FK cruzada
    turma_id = Column(Integer, nullable=False)

    def __repr__(self):
        return f'<Reserva {self.num_sala}>'
    
    
    
    def to_dict(self):
        return {
            'id': self.id,
            'num_sala': self.num_sala,
            'lab': self.lab,
            'data': self.data.isoformat() if self.data else None,
            'turma_id': self.turma_id
        }