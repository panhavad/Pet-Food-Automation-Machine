

def web_wifi_config():
  list_of_wifi = wifi_lookup()
  if get_current_ip() == "0.0.0.0":
    current_wifi, current_ip = "Cannot Connect to " + get_current_wifi(), ""
  else:
    current_wifi, current_ip = "Connected to " + get_current_wifi(), "IP: " + get_current_ip()

  html = """
  <html>
    <head>
      <title>DFA - Home</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="icon" href="data:,">
        <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
        h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
        border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
        .button2{background-color: #4286f4;}
 
        </style>
      </head>
      <body>
        <h1>Wifi Configuration</h1>
        <p><strong>"""+ current_wifi +"""</strong></p>
        <p><strong>"""+ current_ip +"""</strong></p>
          <form action="/">
            <p>
              <select name="wifi_name">
                <option value="" disabled selected>Please select the WIFI</option>
                """+ list_of_wifi +"""
              </select>
            </p>
            <p>
            <input type="password" placeholder="password">
            </p>
        <input type="submit" value="Connect" class="button">
        </form>

      </body>
  """
  
  return html
  
def feed_page(str_lastest_feed):

  html = """<html><head> <title>DFA - Home</title> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  .button2{background-color: #4286f4;}</style></head><body> <h1>Dog Food Automation</h1> 
  <p>Last feed on: <strong>"""+ str_lastest_feed +"""</strong></p><p><a href="/?feed=true"><button class="button">Feed</button></a></p>
  <p>"""
  return html
  
def feed_success_page():
  
  html = """<html><head> <title>DFA - Done</title> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  .button2{background-color: #4286f4;}</style></head><body> <h1>Dog Food Automation</h1> 
  <p><strong>Thank You :)</strong><p><a href="/"><button class="button button2">Home</button></a></p></body></html>"""
  return html

def post_data(payload):
  url = 'http://10.10.11.137/posts/dfa/v0.1' #Change here
  headers = {'content-type': 'application/json'} #Allow to pass JSON data with HTTPS protocol

  try:
    response = urequests.post(url, data = payload, headers = headers)
    parsed = response.json()
    if parsed['code'] == 200:
      print("Posted Successfully.")
    else:
      print("!!Posted Failed!!")
    response.close()
    return True
  except Exception as e:
    print("!!Posted Failed!! - ", e)
    response.close()
    return False  
  
def lastest_feed():
  url = 'http://10.10.11.137/gets/dfa/v0.1/lastest?count=1' #Change here

  response = urequests.get(url)
  for key_name in response.json().keys():
      feed_datetime = key_name
      
  return feed_datetime
  
def get_current_ip():
  current_ip = station.ifconfig()[0]
  return current_ip
  
def get_current_wifi():
  with open("wifi_config.txt","r") as file:
    config_ssid = file.read()
  return config_ssid

def wifi_lookup():
  global wifi_list
  wifi_list, list_of_wifi, nets = [], """""", station.scan()
  for net in nets:
    wifi_name = net[0].decode('UTF-8')
    wifi_list.append(wifi_name.replace(" ", "+") + " ")
    list_of_wifi += "<option value=\"" + wifi_name + "\">" + net[0].decode('UTF-8') + "</option>"
  return list_of_wifi
  
def connect_to_wifi(request):
  wifi_params = request.find("/?wifi_name=")
  if wifi_params == 6:
    for wifi in wifi_list:
      wifi_name = request.find(wifi)
      if wifi_name == 18:
        ssid = wifi.replace(" ","").replace("+", " ")
        with open("wifi_config.txt","w+") as file:
          file.write(ssid)
        rst.value(0)
  else: 
    return web_wifi_config()
 
def move_servo():
  global i
  if i < 100: #less than 180 degree
    while i < 100:
      servo.duty(i)
      i += 1
      utime.sleep_ms(100)
      if i == 100:
        servo.duty(0)
  else:
    while i > 25:
      servo.duty(i)
      i -= 1
      utime.sleep_ms(100)
      if i == 25:
        servo.duty(0)

while True:
  feed_data = dict()
  try:
    prim_conn, prim_addr = prim_socket.accept()
    print('Got a connection from %s' % str(prim_addr))
    request = str(prim_conn.recv(1024))
    response = connect_to_wifi(request)
    prim_conn.send('HTTP/1.1 200 OK\n')
    prim_conn.send('Content-Type: text/html\n')
    prim_conn.send('Connection: close\n\n')
    prim_conn.sendall(response)
    prim_conn.close()
  except Exception as e:
    try:
      conn, addr = s.accept()
      print('Got a connection from %s' % str(addr))
      request = conn.recv(1024)
      request = str(request)
      print('Content = %s' % request)
      feed = request.find('/?feed=true')
      if feed == 6:
        print("Feeding...")
        move_servo()
        feed_data["remote_source"] = str(addr[0])
        feed_data["location"] = "Dog House 01"
        json_data_package = ujson.dumps(feed_data)
        post_data(json_data_package)
        response = feed_success_page()
      else:
        str_lastest_feed = lastest_feed()
        response = feed_page(str_lastest_feed)
      conn.send('HTTP/1.1 200 OK\n')
      conn.send('Content-Type: text/html\n')
      conn.send('Connection: close\n\n')
      conn.sendall(response)
      conn.close()
    except Exception as e:
      pass


