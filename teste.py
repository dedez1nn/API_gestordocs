from config import bcrypt_context

senha = "senha123"

senha_criptografada = bcrypt_context.hash(senha)

print(senha_criptografada)