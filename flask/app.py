from flask import Flask
import __init__

if __name__ == '__main__':
    app = __init__.init_app()
    app.DEBUG=True
    app.run()