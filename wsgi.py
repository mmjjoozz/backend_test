from app.api import create_app
from app.config import DevConfig

app = create_app()

if __name__ == "__main__":
    app.run()
