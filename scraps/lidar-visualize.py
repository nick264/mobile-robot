import pygame
import time
import csv
import math
import sys

# with open('../media/lidar-measurements.csv','rU')  as  csvfile:
#   for row in csv.reader(csvfile,dialect=csv.excel,delimiter=',', quotechar='"'):
#     for elem in row:
#       elem = elem.replace("\ufeff","")
#       sys.stdout.write("%s " % float(elem))
  
#   sys.stdout.write("\n")

pygame.init()

WIDTH            = 1024
HEIGHT           = 768
PIXELS_PER_METER = 100
PI               = 3.14159265

screen = pygame.display.set_mode((WIDTH,HEIGHT))
screen.fill((30,30,30))

with open('./media/lidar-measurements.csv','rU')  as  csvfile:
  for row in csv.reader(csvfile,dialect=csv.excel,delimiter=',', quotechar='"'):
    index = int(row[0].replace("\ufeff",""))
    dataNum = int(row[2].replace("\ufeff",""))
    distance = float(row[3].replace("\ufeff",""))
    error = int(row[4].replace("\ufeff",""))

    if error > 0:
      print("error here")
      continue
      
    degree = index * 4 + dataNum
    rad = degree/360 * 2 * PI
          
    x = WIDTH/2 + math.sin(rad) * distance / 1000 * PIXELS_PER_METER
    y = HEIGHT/2 + math.cos(rad) * distance / 1000 * PIXELS_PER_METER
    
    print((x,y))
    screen.set_at((int(round(x)),int(round(y))),(180,180,255))

pygame.display.flip()
pygame.event.get()

time.sleep(10000)