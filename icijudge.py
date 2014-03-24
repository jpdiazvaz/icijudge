from bottle import route, run, get, static_file, template, request

import os
import subprocess

# Static Paths
@get('/bootstrap/<path:path>')
def bootstrap(path):
	return static_file(path, root='static/bootstrap')
@get('/<filename:re:.*\.css>')
def stylesheet(filename):
	return static_file(filename, root='static/css')
@get('/<filename:re:.*\.js>')
def javascript(filename):
	return static_file(filename, root='static/js')

# Index
@route('/')
def index():
	return template('views/index.html')

# File Upload
@route('/upload', method='POST')
def upload():
	problem_id 	= request.forms.get('problem_id')
	upload		= request.files.get('upload')
	name, ext	= os.path.splitext(upload.filename)
	
	save_path 	= 'submissions/'+problem_id
	full_path 	= save_path+'/'+name+ext
	input_path  = 'problems/'+problem_id+'/input.txt'
	output_path = 'problems/'+problem_id+'/output.txt'

	if not os.path.exists(save_path):
		os.makedirs(save_path)
	upload.save(save_path)

	print full_path
	child = subprocess.Popen(['python '+ full_path + ' < '+input_path],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	output_file = file(output_path)
	for line_file in output_file:
		line_stdout = child.stdout.readline()
		print 'file: '+line_file
		print 'process: '+line_stdout
		if line_file != line_stdout:
			return 'NO'

	return 'OK'


run(host='localhost', port=8080, debug=True)
