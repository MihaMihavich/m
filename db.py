import os
import mysql.connector


class Database(object):
    def __init__(self):
        self.conn = mysql.connector.connect(
            database=str(os.environ.get('database')),
            user=str(os.environ.get('user')),
            password=str(os.environ.get('password')),
            host=str(os.environ.get('host')),
            port=str(os.environ.get('port'))
        )
        self.curs = self.conn.cursor(dictionary=True)

    def __enter__(self):
        return self.curs

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

def add_user(name, sname, fname, passid, country, phone, hash):
    with Database() as curs:
        _SQL = f"""INSERT INTO clients (name, surname, fathername, passportid, country, phone_number, password)
                   VALUES ('{name}', '{sname}', '{fname}', '{passid}', '{country}', '{phone}', '{hash}');"""
        curs.execute(_SQL)

def get_user_by_phone(phone):
    with Database() as curs:
        _SQL = f"""SELECT * FROM clients WHERE phone_number = '{phone}' LIMIT 1;"""
        curs.execute(_SQL)
        return curs.fetchone()

def get_car_types():
    with Database() as curs:
        _SQL = f"""SELECT * FROM car_type;"""
        curs.execute(_SQL)
        return curs.fetchall()
    
def get_life_types():
    with Database() as curs:
        _SQL = f"""SELECT * FROM life_type;"""
        curs.execute(_SQL)
        return curs.fetchall()

def add_life_en(iduser, iden):
    with Database() as curs:
        _SQL = f"""INSERT INTO user_life (iduser, idtype)
            VALUES ({iduser}, {iden});"""
        curs.execute(_SQL)

def add_car_en(iduser, iden, idcar):
    with Database() as curs:
        _SQL = f"""INSERT INTO user_car (iduser, idtype, idcar)
            VALUES ({iduser}, {iden}, {idcar});"""
        curs.execute(_SQL)

def add_car(vin, num, mark, mod, year):
    with Database() as curs:
        _SQL = f"""INSERT INTO cars (vin, number, mark, model, year)
            VALUES ('{vin}', '{num}', '{mark}', '{mod}', {year});"""
        curs.execute(_SQL)

def get_car_id(vin):
    with Database() as curs:
        _SQL = f"""SELECT id FROM cars where vin = '{vin}';"""
        curs.execute(_SQL)
        return curs.fetchone()

def get_my_life(id):
    with Database() as curs:
        _SQL = f"""SELECT name, timing FROM user_life INNER JOIN life_type ON user_life.idtype = life_type.id and user_life.iduser = {id};"""
        curs.execute(_SQL)
        return curs.fetchall()

def get_my_cars(id):
    with Database() as curs:
        _SQL = f"""SELECT name, timing, mark, number FROM (user_car INNER JOIN car_type ON user_car.idtype = car_type.id and user_car.iduser = {id}) inner join cars on cars.id = user_car.idcar;"""
        curs.execute(_SQL)
        return curs.fetchall()

def get_ens_life(id):
    with Database() as curs:
        _SQL = f"""SELECT * from life_type where id = {id};"""
        curs.execute(_SQL)
        return curs.fetchone()

def get_ens_car(id):
    with Database() as curs:
        _SQL = f"""SELECT * from car_type where id = {id};"""
        curs.execute(_SQL)
        return curs.fetchone()
    


