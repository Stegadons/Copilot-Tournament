from werkzeug.security import generate_password_hash

pwd1 = "admin123"
pwd2 = "supersecret"

hash1 = generate_password_hash(pwd1, method="pbkdf2:sha256", salt_length=16)
hash2 = generate_password_hash(pwd2, method="pbkdf2:sha256", salt_length=16)

print("admin1:", hash1)
print("admin2:", hash2)