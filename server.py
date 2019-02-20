from flask import Flask, render_template, request, redirect, make_response
from string import Template
import requests
import os
import json

data = {}


app = Flask(__name__)

#DONE
@app.route('/')
def home(): 
	if('sillyauth' in request.cookies):
		sillyauth = dict(sillyauth = request.cookies.get("sillyauth"))
		t = requests.get('https://hunter-todo-api.herokuapp.com/todo-item', cookies = sillyauth)
		data = json.loads(t.text)
		return render_template('index.html', todos = data, test = sillyauth)
	else:
		return render_template('login.html')

@app.route('/register', methods = ['POST', 'GET'])
def register():
	if request.method == 'POST':
		payload = Template('{"username": "$t"}').safe_substitute( t = request.form['username'])
		requests.post('https://hunter-todo-api.herokuapp.com/user', data = payload)
		return redirect('/')
	else:
		return render_template('register.html')	

@app.route('/login', methods = ['POST'])
def setcookie():
   payload = Template('{"username": "$t"}').safe_substitute( t = request.form['username'])
   r = requests.post('https://hunter-todo-api.herokuapp.com/auth', data = payload)
   cookie = json.loads(r.text)
   resp = make_response(redirect('/'))
   resp.set_cookie('sillyauth', cookie['token'])
   return resp 

@app.route('/logout')
def logout():
	resp = make_response(redirect('/'))
	resp.set_cookie('sillyauth', expires=0)
	return resp
	
@app.route('/add-item', methods=['POST'])
def add_item():
	sillyauth = dict(sillyauth = request.cookies.get("sillyauth"))
	if request.form['item']:
		payload = Template('{"content": "$t" }').safe_substitute( t = request.form['item'])
		requests.post('https://hunter-todo-api.herokuapp.com/todo-item', data = payload, cookies = sillyauth)
	return redirect('/')

@app.route('/delete/<task>')
def delete_task(task):
	sillyauth = dict(sillyauth = request.cookies.get("sillyauth"))
	requests.delete('https://hunter-todo-api.herokuapp.com/todo-item/{}'.format(task),cookies = sillyauth)
	return redirect('/')

@app.route('/flip_true/<task>')
def flip_task_true(task):
    sillyauth = dict(sillyauth = request.cookies.get("sillyauth"))
    print(data)
    payload ='{"completed": true }'
    requests.put('https://hunter-todo-api.herokuapp.com/todo-item/{}'.format(task), data = payload, cookies = sillyauth)
    return redirect('/')

@app.route('/flip_false/<task>')
def flip_task_false(task):
    sillyauth = dict(sillyauth = request.cookies.get("sillyauth"))
    payload ='{"completed": false }'
    requests.put('https://hunter-todo-api.herokuapp.com/todo-item/{}'.format(task), data = payload, cookies = sillyauth)
    return redirect('/')


if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host="0.0.0.0", port=port, threaded=True)




