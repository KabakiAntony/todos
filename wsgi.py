from app import create_app

app = create_app()


@app.route('/')
def root():
    """
    this is the root of our app
    """
    return "<h1>Welcome to todos API</h1>"


if __name__ == "__main__":
    app.run()
