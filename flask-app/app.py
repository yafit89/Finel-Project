from app import create_app

# Create the Flask app using the factory function
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)