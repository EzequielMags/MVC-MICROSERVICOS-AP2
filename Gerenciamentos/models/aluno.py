from models import db 
from sqlalchemy import Column, Integer, ForeignKey, VARCHAR, DATE
from sqlalchemy.orm import relationship 

class Aluno(db.Model):
    __tablename__ = "aluno"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(VARCHAR(100), nullable=False)
    idade = Column(Integer, nullable=False)
    turma_id = Column(Integer, ForeignKey("turma.id"), nullable=False)
    data_nascimento = Column(DATE, nullable=False)
    
    # Relacionamento com Turma (muitos alunos pertencem a uma turma)
    turma = relationship("Turma", back_populates="alunos")
    
    def __repr__(self):
        return f'<Aluno {self.nome}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'idade': self.idade,
            'turma_id': self.turma_id,
            'data_nascimento': self.data_nascimento.isoformat() if self.data_nascimento else None,
            'turma': self.turma.to_dict() if self.turma else None
        }
