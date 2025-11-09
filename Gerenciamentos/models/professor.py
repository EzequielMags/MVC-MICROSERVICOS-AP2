from models import db 
from sqlalchemy import Column, Integer, String, ForeignKey, VARCHAR, TEXT
from sqlalchemy.orm import relationship 


class Professor(db.Model):
    __tablename__ = "professor"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(VARCHAR(100), nullable=False)
    idade = Column(Integer, nullable=False)
    materia = Column(VARCHAR(100), nullable=False)
    observacoes = Column(TEXT, nullable=True)
    
    # Relacionamento com Turma (um professor pode ter várias turmas)
    turmas = relationship("Turma", back_populates="professor", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Professor {self.nome}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'idade': self.idade,
            'materia': self.materia,
            'observacoes': self.observacoes
        }