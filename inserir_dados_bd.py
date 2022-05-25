import configparser
from distutils.command.config import config
from select import select
import sqlalchemy, util, requests, json, string
import pandas as pd
from datetime import datetime, date
from dateutil import relativedelta


def requisitaJSON():
    url = "https://mlb-data.p.rapidapi.com/json/named.roster_team_alltime.bam"
    querystring = {f"start_season":"'2016'","team_id":"'121'","end_season":"'2017'","sort_order":"name_asc","all_star_sw":"'N'"}
    config_object = configparser.ConfigParser()
    config_object.read("configfile.ini")
    apiparam = config_object["api"]
    host = apiparam['X-RapidAPI-Host']
    key = apiparam['X-RapidAPI-Key']
    headers = {
        
        "X-RapidAPI-Host": host,
        "X-RapidAPI-Key": key
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    
    x = response.json()
    return x


def filtraJSON(pessoas):
    inserts = list()
    pessoas = pessoas['roster_team_alltime']['queryResults']['row']
    for pessoa in pessoas:
        nome= str(pessoa['name_last_first']).split(",")
        ultimo, primeiro = nome[0], nome[1]
        n = pessoa['birth_date']
        nascimento = datetime.strptime(n[:10], '%Y-%m-%d').date()
        idade = (relativedelta.relativedelta(date.today(), nascimento)).years
        inserir = dict()
        inserir['ultimo'] = ultimo
        inserir['primeiro'] = primeiro
        inserir['idade'] = idade
        inserts.append(inserir)

    return inserts



def variaveisTabelaPlano(engine):
    inicio, fim = 0, 0
    with engine.connect() as conn:
        query1 = conn.execute(sqlalchemy.text("select idcliente FROM plano order by idcliente DESC limit 1;"))
        query2 = conn.execute(sqlalchemy.text("select count(*) FROM cliente;"))
        conn.close()
        r1 = query1.all()
        r2 = query2.all()
        if len(r1) == 0: 
            inicio = 0
        else:
            for x in r1:
                inicio = x[1]
        if len(r2) == 0: 
            fim = 0
        else:
            
            for x in r2:
                fim = x[0]
        lif = [inicio, fim]

    return lif




def populaTabelaPlano(engine, var):
    with engine.connect() as conn:
        if var[0] == 0:
            var[0] +=1
        for i in range(var[0], var[1]+1):
            di = util.randomData()
            df = util.randomData(di[8:], di[5:7], di[:4])
            
            query1 = conn.execute(sqlalchemy.text(f"insert into plano(idcliente, inicioPlano, UltimoPagamento) VALUES ('{i}','{di}', '{df}');"))
        conn.close()
    return 'success!'
    






def acessaBanco(engine, filtrado):
    
    with engine.connect() as conn:
        for pessoa in filtrado:
            ultimo = pessoa['ultimo'].replace("'", "")

            result = conn.execute(sqlalchemy.text(f"insert into cliente(PrimeiroNome, UltimoNome, Idade) VALUES ('{pessoa['primeiro']}','{ultimo}', '{pessoa['idade']}');"))
        conn.close()
    return 'inseriu'







if __name__ == '__main__':
        dados = requisitaJSON()
        filtrado = filtraJSON(dados)
        conexao = util.conectaBD()
        acessaBanco(conexao, filtrado)
        z = variaveisTabelaPlano(conexao)
        populaTabelaPlano(conexao, z)

