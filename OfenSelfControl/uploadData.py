# importing the requests library 
import requests 
  
# defining the api-endpoint  
API_ENDPOINT = "http://ofenwatch.woller.pizza/yamifood/php/ofenwatch/process_incoming_data.php"
  
# your API key here 
API_KEY = "XXXXXXXXXXXXXXXXX"
  
# your source code here 
source_code = ''' 
print("Hello, world!") 
a = 1 
b = 2 
print(a + b) 
'''
  
# data to be sent to api 
data = {'ofenid':'101', 
        'temp1':'100', 
        'temp2':'200', 
        'temp3':'300',
        'temp4':'400'} 
  
# sending post request and saving response as response object 
r = requests.post(url = API_ENDPOINT, data = data) 
  
# extracting response text  
pastebin_url = r.text 
print("Response:%s"%pastebin_url) 
