from flask import Flask,request
from json import loads

app=Flask(__name__)

@app.route('/',methods=['POST'])
def server():
	data=request.get_data().decode('utf-8')
	data=loads(data)
	print(data)
	msg=data['raw_message']
	print('\n' + msg +'\n')
	return '200 OK'

if __name__ == '__main__':
	app.run()