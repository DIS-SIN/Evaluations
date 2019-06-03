from flask import Flask

def init_schemas(app: Flask):
    from .dump_schemas import init_dump_schemas
    from .load_schemas import init_load_schemas
    init_dump_schemas(app)
    init_load_schemas()

