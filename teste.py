from config import bcrypt_context

senha = "sergioaislan"
senha2 = "matheusmendes"

senha_criptografada = bcrypt_context.hash(senha)
senha_criptografada2 = bcrypt_context.hash(senha2)

print(senha_criptografada)
print(senha_criptografada2)