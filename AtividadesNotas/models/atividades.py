from models import db 
from sqlalchemy import Column, Integer, String, ForeignKey, VARCHAR, DATE, Float
from sqlalchemy.orm import relationship 
from datetime import date

class Atividades(db.Model):
    __tablename__ = "atividades"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_atividade = Column(VARCHAR(100), nullable=False)
    descricao = Column(VARCHAR(100), nullable=False)
    peso_porcento = Column(Integer, nullable=False)
    data_entrega = Column(DATE, nullable=False)
    # IDs referenciais para serviços externos (sem FK entre bancos)
    professor_id = Column(Integer, nullable=False)
    turma_id = Column(Integer, nullable=False)
    def __repr__(self):
        return f'<Atividade {self.nome}>'
    
    
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome_atividade': self.nome_atividade,
            'descricao': self.descricao,
            'peso_porcento': self.peso_porcento,
            'data_entrega': self.data_entrega.isoformat() if self.data_entrega else None,
            'professor_id': self.professor_id,
            'turma_id': self.turma_id
        }