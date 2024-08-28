import bcrypt 

def encrypt_pass(senha: str)->str:
    senha_bytes = senha.encode('utf-8')
    # Gera o salt e o hash da senha
    senha_hash = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
    # Retorna o hash como uma string
    return senha_hash.decode('utf-8')

def decrypt_pass(senha:str, key:str)->bool:
    # Converte a senha e o hash codificado para bytes
    senha_bytes = senha.encode('utf-8')
    senha_codificada_bytes = key.encode('utf-8')
    # Verifica se a senha corresponde ao hash
    return bcrypt.checkpw(senha_bytes, senha_codificada_bytes)


