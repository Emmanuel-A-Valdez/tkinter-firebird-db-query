from firebird.driver import connect, driver_config


# Register Firebird server
srv_cfg = """[local]
host = localhost
user = SYSDBA
password = masterkey
"""
driver_config.register_server("local", srv_cfg)

# Register database
db_cfg = """[web]
server = local
database = d:/data/web.fdb
protocol = inet
charset = utf8
"""
driver_config.register_database("web", db_cfg)

# Connect to database
con = connect("web")

# Create a Cursor object that operates in the context of Connection con:
cur = con.cursor()