'''
Created on Feb 2, 2017

@author: bbest
'''

# This is a functional main driver

import math, sys
from ClassExample import MyClass

def foo():
  print "a function"

def main():
  #print "This is main"
  #obj = Object.instance()
  #obj.set_some_int(10)
  #print obj.get_some_int()

  rounds = 21
  total = 0
  crit = 0
  
  i = 0
  while(rounds > 0):
    print "Remainder of rounds = ", rounds
    crit = crit + 1
    rounds = rounds - 1
    if(crit == 3):
      rounds = rounds + 1
      crit = 0
    total = total + 1
  print "Total number of rounds = ", total

if __name__ == '__main__':
    main()