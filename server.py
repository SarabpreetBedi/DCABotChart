from flask import Flask, render_template, request
import subprocess
import time 



app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def home():
    return render_template('home.html')

@app.route('/my-link/', methods=['GET', 'POST'])
def my_link():

  print('I got clicked!')    
  subprocess.call("buysell.py", shell=True)
 
  return 'Click.'


if __name__ == '__main__':
  app.run(debug=True)