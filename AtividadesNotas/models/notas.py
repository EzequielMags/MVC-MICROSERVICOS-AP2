from models import db 
from sqlalchemy import Column, Integer, String, ForeignKey, VARCHAR, DATE, Float
from sqlalchemy.orm import relationship 
from datetime import date

class Notas(db.Model):
    __tablename__ = "Notas"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nota =Column(Float, nullable=False)
    # IDs referenciais para serviços externos (sem FK entre bancos)
    aluno_id = Column(Integer, nullable=False)
    # FK local para tabela interna de atividades
    atividade_id = Column(Integer, ForeignKey("atividades.id"), nullable=False)
    atividade = relationship("Atividades")
    def __repr__(self):
        return f'<Notas {self.nota}>'
    
    
    
    def to_dict(self):
        return {
            'id': self.id,
            'nota': self.nota,
            'aluno_id': self.aluno_id,
            'atividade': self.atividade.to_dict() if self.atividade else None
        }