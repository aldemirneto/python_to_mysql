import configparser, sqlalchemy
from distutils.util import execute
import random

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





def randomData(day = 0, month = 0,year = 0):
    if day == 0:
        d =random.randrange(1, 31)
        if d< 10:
            dia = f"0{d}"
        else:
            dia = d
    else:
        d =random.randrange(1, 31)
        if d< 10:
            dia = f"0{d}"
        else:
            dia = d
        

    if month == 0:
        m =  random.randrange(1, 12)
        if m< 10:
            mes = f"0{m}"
        else:
            mes = m
    else:
        if int(month) == 12:
            m =  random.randrange(1, 11)
            if m< 10:
                mes = f"0{m}"
            else:
                mes = m
        else:    
            m =  random.randrange(int(month), 12)
            if m< 10:
                mes = f"0{m}"
            else:
                mes = m
            

    if year == 0:
        y = random.randrange(18, 23)    
        year = int(f"20{y}")
    else:
        y = random.randrange(int(year[2:]), 23)
        year = int(f"20{y}")
     
    data = str(f"{year}-{mes}-{dia}")
    
    return data




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