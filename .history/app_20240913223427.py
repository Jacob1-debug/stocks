from flask import Flask, render_template

# Create a Flask instance
app = Flask(__name__)

# Define a route for the root URL
@app.route('/')
def home():
    return "Hello, World!"

# Define a route for the about page
@app.route('/about')
def about():
    return "This is the about page."

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
