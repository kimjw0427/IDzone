import os

a = os.popen(f'ifconfig').read()

print(a)
print(type(a))