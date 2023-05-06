from flask import Flask, render_template
import json

app=Flask(__name__,template_folder='templates')
@app.route('/')
def show_data():
    # Load JSON data from the file
    with open('email.json') as json_file:
        data = json.load(json_file)

    # Render the template and pass the data to the template
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run()
