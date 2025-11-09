from models import db 
from sqlalchemy import Column, Integer, String, ForeignKey, VARCHAR, TEXT, Boolean
from sqlalchemy.orm import relationship 


class Turma(db.Model):
    __tablename__ = "turma"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(VARCHAR(100), nullable=False)
    professor_id = Column(Integer, ForeignKey("professor.id"), nullable=False)
    ativo = Column(Boolean, nullable=False, default=True)
    
    # Relacionamento com Professor (muitas turmas pertencem a um professor)
    professor = relationship("Professor", back_populates="turmas")
    
    # Relacionamento com Aluno (uma turma pode ter vários alunos)
    alunos = relationship("Aluno", back_populates="turma", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Turma {self.descricao}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'descricao': self.descricao,
            'professor_id': self.professor_id,
            'ativo': self.ativo,
            'professor': self.professor.to_dict() if self.professor else None,
            'total_alunos': len(self.alunos) if self.alunos else 0
        }