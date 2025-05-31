from bson import ObjectId
from config.conexion_mongo import db
from dataclasses import dataclass
from bson import ObjectId


class Base:
    '''
    Clase base que abstrae los atributos y metodos utilitarios
    '''
   


    def __post_init__(self):
        '''
        Metodo de post instanciación para la normalización de los ids
        '''

        if isinstance(self._id, ObjectId):

            self._id = ObjectId(self._id)
        

    def json(self):
        '''
        Hace uso del metodo recursivo remove oids para convertir documentos a tipos de datos
        serializables
        '''
        
        newDoc = self.__dict__.copy()

        return Base.__remove_oid(newDoc)
    
    
    def save(self):

        if not self._id is None:

            result = db[self.__collection__].update_one({'_id':self._id}, {'$set': self.__dict__})
        
            return result.modified_count
        
        else:

            payload = self.__dict__.copy()

            del payload['_id']

            result = db[self.__collection__].insert_one(payload)

            newId = result.inserted_id

            self._id = newId


            return newId


    
        

    @staticmethod
    def __remove_oid(document:dict):

        newDoc = document.copy()

        for key, val in newDoc.items():

            if isinstance(val, ObjectId):

                newDoc[key] = str(val)
            
            if isinstance(val, list):

                for index, item in enumerate(val):

                    newDoc[key][index] = Base.__remove_oid(item)
        
        return newDoc
    

    @classmethod
    def from_list(cls, documents: list[dict]):
        

        if not isinstance(documents, list):

            raise Exception("Se esperaba una lista de diccionarios")
        

        results = [cls(**r) for r in documents]

        return results