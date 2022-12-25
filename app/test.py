from flask import Flask,render_template,request
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/searchByText",methods=['POST'])
def searchByText():
    searchText = request.form['searchText']
    print("当前搜索的图片是："+searchText)
    return render_template('index.html')

if __name__ == "__main__":
    app.run()