from firebird.driver import connect, driver_config


# Register Firebird server
srv_cfg = """[local]
host = localhost
user = SYSDBA
password = masterkey
"""
driver_config.register_server("local", srv_cfg)

# Register default database
db_cfg = """[Web]
server = local
database = d:/data/web.fdb
protocol = inet
charset = utf8
"""
driver_config.register_database("Web", db_cfg)

# Register database
db2_cfg = """[El Siglo]
server = local
database = d:/data/deportes_el_siglo.fdb
protocol = inet
charset = utf8
"""
driver_config.register_database("El Siglo", db2_cfg)

# Connect to database
con = connect("Web")

# Create a Cursor object that operates in the context of Connection con:
cur = con.cursor()
