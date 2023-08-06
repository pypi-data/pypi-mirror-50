class BaseError(Exception):
   """Raised when the input value is too small"""
   pass

class CannotConnectMongoDB(Exception):
   """Raised when connection to the database fails"""
   pass

class CannotFindCollection(Exception):
   """Raised when the collection is not found in the database"""
   pass
   pass

class ConfigNotDict(Exception):
   """Raised when the collection is not found in the database"""
   pass