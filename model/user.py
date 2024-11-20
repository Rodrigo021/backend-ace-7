from sqlalchemy import create_engine, Column, Integer, String, ARRAY
from sqlalchemy.orm import sessionmaker, declarative_base
from utils.encode import encrypt_pass, decrypt_pass

# Configuração do SQLAlchemy
DATABASE_URL = "postgresql+psycopg2://seu_usuario:sua_senha@localhost:5432/seu_banco"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo do usuário
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    sistema = Column(ARRAY(Integer), nullable=False)
    cargos_do_sistema = Column(ARRAY(Integer), nullable=False)

# Criação da tabela no banco de dados (caso ainda não exista)
Base.metadata.create_all(bind=engine)

# Sistema de Login
class SistemaLogin:
    def __init__(self):
        self.db = SessionLocal()
    
    def cadastrar_usuario(self, nome, senha, sistema, cargos_do_sistema):
        try:
            usuario = Usuario(
                nome=nome,
                senha=encrypt_pass(senha=senha),
                sistema=sistema,
                cargos_do_sistema=cargos_do_sistema,
            )
            self.db.add(usuario)
            self.db.commit()
            print("Usuário cadastrado com sucesso!")
        except Exception as e:
            self.db.rollback()
            print(f"Erro ao cadastrar usuário: {e}")
        finally:
            self.db.close()
    
    def atualizar_usuario(self, user_id, nome=None, senha=None, sistema=None, cargos_do_sistema=None):
        try:
            usuario = self.db.query(Usuario).filter(Usuario.id == user_id).first()
            if usuario:
                if nome:
                    usuario.nome = nome
                if senha:
                    usuario.senha = encrypt_pass(senha)
                if sistema is not None:
                    usuario.sistema = sistema
                if cargos_do_sistema is not None:
                    usuario.cargos_do_sistema = cargos_do_sistema
                self.db.commit()
                print("Usuário atualizado com sucesso!")
            else:
                print("Usuário não encontrado.")
        except Exception as e:
            self.db.rollback()
            print(f"Erro ao atualizar usuário: {e}")
        finally:
            self.db.close()
    
    def deletar_usuario(self, user_id):
        try:
            usuario = self.db.query(Usuario).filter(Usuario.id == user_id).first()
            if usuario:
                self.db.delete(usuario)
                self.db.commit()
                print("Usuário deletado com sucesso!")
            else:
                print("Usuário não encontrado.")
        except Exception as e:
            self.db.rollback()
            print(f"Erro ao deletar usuário: {e}")
        finally:
            self.db.close()
    
    def autenticar(self, nome, senha):
        try:
            usuario = self.db.query(Usuario).filter(Usuario.nome == nome).first()
            if usuario and decrypt_pass(senha, usuario.senha):
                return True
            return False
        except Exception as e:
            print(f"Erro ao autenticar usuário: {e}")
            return False
        finally:
            self.db.close()
    
    def obter_id(self, user_nome):
        try:
            usuario = self.db.query(Usuario).filter(Usuario.nome == user_nome).first()
            if usuario:
                return usuario.id
            return None
        except Exception as e:
            print(f"Erro ao obter id: {e}")
            return None
        finally:
            self.db.close()
    
    def obter_nome(self, user_id):
        try:
            usuario = self.db.query(Usuario).filter(Usuario.id == user_id).first()
            if usuario:
                return usuario.nome
            return None
        except Exception as e:
            print(f"Erro ao obter nome: {e}")
            return None
        finally:
            self.db.close()
    
    def obter_sistema(self, user_id):
        try:
            usuario = self.db.query(Usuario).filter(Usuario.id == user_id).first()
            if usuario:
                return usuario.sistema
            return None
        except Exception as e:
            print(f"Erro ao obter sistemas: {e}")
            return None
        finally:
            self.db.close()
    
    def obter_cargos_do_sistema(self, user_id):
        try:
            usuario = self.db.query(Usuario).filter(Usuario.id == user_id).first()
            if usuario:
                return usuario.cargos_do_sistema
            return None
        except Exception as e:
            print(f"Erro ao obter cargos do sistema: {e}")
            return None
        finally:
            self.db.close()
