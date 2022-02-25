from app import create_app
from flask import render_template

app = create_app()


@app.route('/')
def root():
    """
    this is the root of our app
    """
    return render_template('index.html')


if __name__ == "__main__":
    app.run()
