from config import bcrypt_context

senha_plana = "tripax321"
hash = bcrypt_context.hash(senha_plana)
print(hash)
