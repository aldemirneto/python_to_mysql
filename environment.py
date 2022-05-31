import configparser, sqlalchemy
def conectaBD():
    config_obj = configparser.ConfigParser()
    config_obj.read("configfile.ini")
    dbparam = config_obj["mysql-inserir"]    
    user = dbparam["user"]
    password = dbparam["password"]
    host = dbparam["host"]
    port = int(dbparam["port"])
    
    dbase = dbparam["db"]
    engine = sqlalchemy.create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{dbase}",encoding='utf8' ,echo = True)
    return engine




def createDB():
    engine = conectaBD()
    with engine.connect() as conn:
        conn.execute(sqlalchemy.text("DROP TABLE IF EXISTS `cliente`;"))
        conn.execute(sqlalchemy.text("""
        CREATE TABLE `cliente` (
        `IdCliente` int NOT NULL AUTO_INCREMENT,
        `PrimeiroNome` varchar(255) NOT NULL,
        `UltimoNome` varchar(255) NOT NULL,
        `Idade` int DEFAULT NULL,
        PRIMARY KEY (`IdCliente`)
        ) 

        """))
        conn.execute(sqlalchemy.text("DROP TABLE IF EXISTS `plano`;"))
        conn.execute(sqlalchemy.text("""
        CREATE TABLE `plano` (
        `idplano` int NOT NULL AUTO_INCREMENT,
        `idcliente` int NOT NULL,
        `InicioPlano` date NOT NULL,
        `UltimoPagamento` date NOT NULL,
        PRIMARY KEY (`idplano`)
        ) """
        ))
        conn.close()
