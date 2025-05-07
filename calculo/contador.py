import time

cuenta = 0
def contador():
  global cuenta
  time.sleep(1)
  cuenta+=1

for i in range(1000):
  contador()
  print(cuenta)
