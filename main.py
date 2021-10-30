import urllib.request
import urllib.parse
 
def sendSMS(apikey, numbers, sender, message="Hi there, thank you for sending your first test message from Textlocal. Get 20% off today with our code:"):
    data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
        'message' : message, 'sender': sender, 'test' : True})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return(fr)
 
resp =  sendSMS('NTI1NzQ4NDQ3NzczNjI2ZTQ0NjE0YTU0NDk1NjYzNDE=', '919398544577',
    'Jims Autos')
print (resp)
