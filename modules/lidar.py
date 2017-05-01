import time
import RPi.GPIO as GPIO
import serial
import sys
import csv
import os
import pygame
import math

PI = 3.14159265

class Lidar:
  def __init__(self):
    self.serial_rx_pin     = 15
    self.motor_trigger_pin = 26
    
    # configure serial read
    self.serial = serial.Serial('/dev/ttyAMA0', 115200) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.

    # configure GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.motor_trigger_pin, GPIO.OUT, initial=GPIO.LOW)

    # configure display
    self.display_width            = 480
    self.display_height           = 320
    self.display_pixels_per_meter = 50
    os.putenv('SDL_FBDEV', '/dev/fb1') # output to LCD touchscreen
    pygame.init()
    self.screen = pygame.display.set_mode((self.display_width,self.display_height))

  def terminate(self):
    sys.stdout.write("Closing serial port...")
    self.serial.flushInput()
    self.serial.close()
    sys.stdout.write("done\n")
    GPIO.cleanup()  

  # packet format -- 22 bytes:
  # 0       1       2         3          4        8        12       16      20            21
  # <start> <index> <speed_L> <speed_H> [Data 0] [Data 1] [Data 2] [Data 3] <checksum_L> <checksum_H>
  def processRotation(self,data):
    good_sets = 0
    bad_sets = 0
    
    # # print all the data
    # for i in xrange(len(data) / 22):
    #   for j in xrange(22):
    #     sys.stdout.write(hex(ord(data[i*22 + j])))
    #     sys.stdout.write(" ")
    #   sys.stdout.write("\n")
    
    processed_data = []
    
    for i in xrange(len(data) / 22):
      # get index
      if ord(data[i*22 + 1]) == 0xA0 + i:
        # print("i = ", i, ": good")
        good_sets += 1
      else:
        # print("i = ", i, ": expected ", hex(0xA0 + i), ", got ", hex(ord(data[i*22 + j])))
        bad_sets += 1
        
      index = ord(data[i*22 + 1]) - 0xA0

      # get rpm
      speed_l = ord(data[i*22 + 2])
      speed_h = ord(data[i*22 + 3])
      
      rpm = ( ( speed_h << 8 ) | speed_l ) / 64.0
      
      for dataNum in xrange(4):
        # get distance
        byte0 = ord(data[i*22 + 4 + dataNum * 4 + 0])
        byte1 = ord(data[i*22 + 4 + dataNum * 4 + 1])
        byte2 = ord(data[i*22 + 4 + dataNum * 4 + 2])
        byte3 = ord(data[i*22 + 4 + dataNum * 4 + 3])
        
        flag0 = ( byte1 & 0x80 ) << 7 # No return/max range/too low of reflectivity
        flag1 = ( byte1 & 0x40 ) << 6 # Object too close, possible poor reading due to proximity kicks in
        distance = ( ( byte1 & 0x3f ) << 8 ) | byte0
        
        processed_data.append([index, rpm, dataNum, distance, flag0, flag1 ])
      
    print("good_sets = ", good_sets)
    print("bad_sets = ", bad_sets)
    
    # print("Processed data:")
    # for i in xrange(len(processed_data)):
    #   for j in xrange(len(processed_data[i])):
    #     sys.stdout.write("%s " % processed_data[i][j])
    #   sys.stdout.write("\n")
    return processed_data
  
  def startReading(self):
    try:
      # turn on motor
      sys.stdout.write("Turning on motor...\n")
      GPIO.output(self.motor_trigger_pin, GPIO.HIGH)
      time.sleep(2)
      
      # reading 
      sys.stdout.write("Reading data...\n")
      self.serial.flushInput()
      
      cycles_read = 0
      while True:
          bytesToRead = self.serial.inWaiting()
          
          if bytesToRead > 0:
            byte = self.serial.read(1)
            
            if ord(byte) == 0xFA:
              # sys.stdout.write("got a new packet\n")  
              
              index_byte = self.serial.read(1)
              
              if ord(index_byte) == 0xA0:
                sys.stdout.write("Got beginning of rotation\n")
                
                # process and display data
                data = self.processRotation(byte + index_byte + self.serial.read(1978))
                self.displayData(data)
                
                # process pygame event loop                
                for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                    print("got quit event")
                    self.terminate()
                  if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    print("got q keyboard press")
                    pygame.quit()
                    self.terminate()
                
                cycles_read += 1
                print("read cycle")
            
            # if packet_pos != None and packet_pos == 1:
            #   sys.stdout.write("packet #:" + hex(ord(data)) + "\n")
            
            # if packet_pos != None:
            #   packet_pos += 1
            
            # sys.stdout.write(hex(ord(data)))
            sys.stdout.flush()
    except KeyboardInterrupt:
      self.terminate()
  
  def displayData(self,data):
    self.screen.fill((15,15,15))
    self.plotData(data)
    pygame.display.flip()

  def testData(self):
    retData = []
    with open('./media/lidar-measurements.csv','rU')  as  csvfile:
      for row in csv.reader(csvfile,dialect=csv.excel,delimiter=',', quotechar='"'):
        fixed_data = list(map(lambda x: float(x.replace("\ufeff","")),row))
        retData.append(fixed_data)
    return retData
  
  def plotData(self,data):
    for d in data:
      print(d)
      # skip if error
      if d[4] > 0:
        continue
      
      distance = d[3]
      degree   = d[0] * 4 + d[2]
      rad      = degree/360.0 * 2.0 * PI
      
      x = self.display_width/2.0 + ( math.sin(rad) * distance / 1000.0 * self.display_pixels_per_meter )
      y = self.display_height/2.0 + ( math.cos(rad) * distance / 1000.0 * self.display_pixels_per_meter )
      
      print((x,y))
      
      self.screen.set_at((int(round(x)),int(round(y))),(190,190,255))

# l = Lidar()
# l.startReading()
