from hashing import Hash

password = "Nency@2000"
hashed = Hash.bcrypt(password)
print(f"Original: {password}")
print(f"Hashed: {hashed}")

is_correct = Hash.verify(hashed, "mysecretpassword")
print(f"Is the password correct? {is_correct}")

is_hacker_correct = Hash.verify(hashed, "wrongpassword")
print(f"Is the hacker correct? {is_hacker_correct}")