try:
  import usocket as socket
except:
  import socket

from machine import Pin, PWM
import utime, ujson, network, urequests, json, esp, gc, ure

esp.osdebug(None) 
gc.collect()

with open("wifi_config.txt","r") as file:
  ssid = file.read()
  
password = ''

station = network.WLAN(network.STA_IF)
wifiap = network.WLAN(network.AP_IF)
  
wifiap.active(True)
station.active(True)

prim_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
prim_socket.bind(('0.0.0.0', 88))
prim_socket.settimeout(3)
prim_socket.listen(5)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 80))
s.settimeout(5)
s.listen(5)

wifiap.config(essid="DFA_AP", password="admin123321")
station.connect(ssid, password)

led = Pin(2, Pin.OUT)
rst = Pin(16, Pin.OUT)
wifi_list = []

servo = PWM(Pin(14), freq=40, duty=77)
i = 25
servo.duty(i)





