from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host="10.10.10.10", port=8000, debug=True)
