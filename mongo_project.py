import pymongo
import logging
from decouple import config

username = config('username',default='')
password = config('password',default='')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

f = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh = logging.FileHandler('mongo_activity.log')
fh.setFormatter(f)
logger.addHandler(fh)

class database:
    def __init__(self, dbname,collection) -> None:
        self.dbname = dbname
        self.collection = collection

    @staticmethod
    def connect():
        client = pymongo.MongoClient(
            f"mongodb+srv://{username}:{password}@cluster0.5vtnaax.mongodb.net/?retryWrites=true&w=majority")
        return client
    
    def insert(self,data:list):
        logger.info('Uploading record to collection....')
        client = database.connect()
        dbase = client[self.dbname]
        col = dbase[self.collection]
        try:
            col.insert_many(data)
        except Exception as e:
            logger.error(e)
        finally:
            logger.info("Records uploaded")


    def update(self,colname,old_value,new_value):
        logger.info(f'Updating a record with value: {new_value}....')
        client = database.connect()
        dbase = client[self.dbname]
        col = dbase[self.collection]
        try:
            col.update_one({colname:old_value} , {'$set':{colname : new_value}})
        except Exception as e:
            logger.error(e)
        else:
            logger.info("Record updated")

    def delete(self,colname,value):
        logger.info('Deleting a record....')
        client = database.connect()
        dbase = client[self.dbname]
        col = dbase[self.collection]
        try:
            col.delete_one({colname:value})
        except Exception as e:
            logger.error(e)
        else:
            logger.info("Successfully deleted a record from the collection")

def read_file(file_path:str) -> tuple:
    """
    Function to read a file into buffer
    Parameter: 
        file_path: directory to file
    Returns:
        tuple(header,body)
    """
    logger.info("Reading from file")
    try:
        with open(file_path, 'r') as file:
            data = file.readlines()
    except Exception as e:
        logger.error(e)
    else:
        body = list()
        for line in data:
            body.append(line.strip())
        body = [line.split(',') for line in body]
        header = body.pop(0)
        logger.info("Changing column name index to indx")
        header[0] = 'indx'
    return header, body

def convert_dtype(data) -> list:
    logger.info("Converting string datatype to int and float....")
    try:
        for item in data:
            for i in range(len(item)):
                if i == 0 or i== 10:
                    item[i] = int(item[i])
                else:
                    item[i] = float(item[i])
    except Exception as e:
        logger.error(e)
    else:
        data = [tuple(item) for item in data]
        logger.info("Data successfuly converted")

    return data

def list_of_dict(keys, values):
    logger.info("Converting record to list of dictionaries")
    try:
        lst = list()
        for item in values:
            temp = {keys[i]:item[i] for i in range(len(item))}
            lst.append(temp)
    except Exception as e:
        logger.error(e)
    else:
        logger.info("Conversion completed")
        return lst

db_name = 'property'
db_col= 'glass'
db = database(db_name,db_col)

#read data out of file
head,body = read_file('mongo_db/glass.txt')

#convert from string to int,float
body = convert_dtype(body)

# create list of dictionaries from the records. Data structure for MongoDb insertion
records = list_of_dict(head, body)

#insertion of records
db.insert(records)

#update records
db.update('Na',13,9)

#delete record
db.delete('Na', 9)