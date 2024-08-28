from sqlalchemy import create_engine, Column, Integer, String, ARRAY
from sqlalchemy.orm import sessionmaker, declarative_base
from utils.encode import encrypt_pass, decrypt_pass

# Configuração do SQLAlchemy
DATABASE_URL = "postgresql+psycopg2://postgres:Rodrigo2003@localhost:5432/ace"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo do usuário
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    cargo = Column(ARRAY(Integer), nullable=False)

# Criação da tabela no banco de dados (caso ainda não exista)
Base.metadata.create_all(bind=engine)

# Sistema de Login
class SistemaLogin:
    def __init__(self):
        self.db = SessionLocal()
    
    def cadastrar_usuario(self, nome, senha, cargo):
        try:
            
            usuario = Usuario(nome=nome, senha=encrypt_pass(senha=senha), cargo=cargo)
            self.db.add(usuario)
            self.db.commit()
            self.db.close()
            print("Usuário cadastrado com sucesso!")
        except Exception as e:
            self.db.rollback()
            self.db.close()
            print(f"Erro ao cadastrar usuário: {e}")
    
    def atualizar_usuario(self, user_id, nome=None, senha=None, cargo=None):
        try:
            usuario = self.db.query(Usuario).filter(Usuario.id == user_id).first()
            if usuario:
                if nome:
                    usuario.nome = nome
                if senha:
                    usuario.senha = encrypt_pass(senha)
                if cargo is not None:
                    usuario.cargo = cargo
                self.db.commit()
                self.db.close()
        except Exception as e:
            self.db.rollback()
            self.db.close()
            print(f"Erro ao atualizar usuário: {e}")
    
    def deletar_usuario(self, user_id):
        try:
            usuario = self.db.query(Usuario).filter(Usuario.id == user_id).first()
            if usuario:
                self.db.delete(usuario)
                self.db.commit()
                self.db.close()
                print("Usuário deletado com sucesso!")
            else:
                print("Usuário não encontrado.")
        except Exception as e:
            self.db.rollback()
            self.db.close()
            print(f"Erro ao deletar usuário: {e}")
    
    def autenticar(self, nome, senha):
        try:
            usuario = self.db.query(Usuario).filter(Usuario.nome == nome).first()
            self.db.close()
            return decrypt_pass(senha,usuario.senha)
        except Exception as e:
            print(f"Erro ao autenticar usuário: {e}")
            self.db.close()
            return False
    
    def obter_id(self, user_nome):
        try:
            usuario = self.db.query(Usuario).filter(Usuario.nome == user_nome).first()
            self.db.close()
            if usuario:
                return usuario.id
            return None
        except Exception as e:
            print(f"Erro ao obter id: {e}")
            self.db.close()
            return None
    
    def obter_nome(self, user_id):
        try:
            usuario = self.db.query(Usuario).filter(Usuario.id == user_id).first()
            self.db.close()
            if usuario:
                return usuario.nome
            return None
        except Exception as e:
            print(f"Erro ao obter nome: {e}")
            self.db.close()
            return None
    
    def obter_cargo(self, user_id):
        try:
            usuario = self.db.query(Usuario).filter(Usuario.id == user_id).first()
            self.db.close()
            if usuario:
                return usuario.cargo
            return None
        except Exception as e:
            print(f"Erro ao obter cargo: {e}")
            self.db.close()
            return None



