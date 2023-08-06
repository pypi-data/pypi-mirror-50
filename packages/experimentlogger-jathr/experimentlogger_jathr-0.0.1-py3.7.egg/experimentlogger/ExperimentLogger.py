from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps, RELAXED_JSON_OPTIONS
from datetime import datetime
import json
from simplejson import loads
from easydict import EasyDict as edict
from experimentlogger.utils.errors import CannotConnectMongoDB, CannotFindCollection, ConfigNotDict
import uuid
import os

def find_experiment_by_id(id):
        client = MongoClient('localhost', 27017)
        db = client.drive_test_measurements
        experiments = db.experiments
        return experiments.find_one({'_id': ObjectId(id) })

def load_training_history(id):
        experiment = find_experiment_by_id(id)
        experiment['training_history']['test_loss'] = experiment['test_loss']
        return experiment['training_history'], experiment['config']['epochs']

def load_experiment(id, root_path='exps/'):
    """
    Load single experiment by ID
    """
    config_path = "{}/{}.json".format(root_path, id)
    with open(config_path) as file:
        data = json.load(file)

    config = data['config']
    results = data['results']
    date = data['date']
    exp = Experiment('file', config=config)
    exp.results = results
    exp.date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    exp.id = id
    
    return exp


def load_experiments(root_path):
    """
    Returns list of experiments from root folder
    """
    list_of_files = os.listdir(root_path) 

    experiments = []
    for file in list_of_files:
        if '.json' in file:
            id = file[:-5]
            exp = load_experiment(id, root_path = root_path)
            experiments.append(exp)

    return experiments
    
        

class Experiment():
    

    def __init__(self, mode, **kwargs):

        if not isinstance(kwargs.get('config'), dict):
            raise ConfigNotDict('Config not a dict')

        self.mode = mode
        self.date = datetime.utcnow()
        self.config = kwargs.get('config')
        self.results = None

        if mode == 'mongodb':
            self.collection_name = kwargs.get('collection_name')
            self.database = kwargs.get('database')
            self.db = None
            self.setup_pymongo()
        elif mode == 'file':
            self.root_folder = kwargs.get('root_folder') if kwargs.get('root_folder') else 'exps/'
            self.id = self._generate_id()

    def __str__(self):
        valid_loss = self.results['valid_loss'] if self.results['valid_loss'] else ''
        return "id: {}, date: {}, valid loss: {}".format(self.id, str(self.date), valid_loss)

    def _generate_id(self):
        return str(uuid.uuid4())

    def setup_pymongo(self):
        client = MongoClient('localhost', 27017)
        self.db = client[self.database]
        self._test_connection()
        self._db_has_collection()
        
    def _test_connection(self):
        try:
            self.db.list_collection_names()
        except:
            raise CannotConnectMongoDB()

    def _db_has_collection(self):
        if self.collection_name not in self.db.list_collection_names():
            raise CannotFindCollection('Cannot find {} in {}'.format(self.collection_name, self.db.list_collection_names()))

    def save(self):
        if self.mode == 'mongo':
            self._store_mongo()
        elif self.mode == 'file':
            self._store_json()
        

    def _store_json(self):
        # Check root folder exist
        if not os.path.isdir(self.root_folder):
            os.mkdir(self.root_folder)

        obj_dict = dict()
        obj_dict['results'] = self.results
        obj_dict['config'] = self.config
        obj_dict['date'] = str(self.date)

        with open("{}/{}.json".format(self.root_folder, self.id), 'w') as file:
            json.dump(obj_dict, file, sort_keys=True, indent=4)


        

    def _store_mongo(self):
        experiments = self.db[self.list_collection_names]
        delattr(self,'collection_name')

        if self.results == None:
            Warning('No results added.')

        experiment_id = experiments.insert_one(self.__dict__).inserted_id
        return experiment_id

    def find_best_model(self, start_date = datetime(2018, 7, 1, 7, 0, 0)):
        experiments = self.db[self.collection_name]    
        filtered_experiments =  experiments.find({'date': {'$gte': start_date}})
        sorted_experiments = filtered_experiments.sort('results.test_loss',1)
        return sorted_experiments[0]


def test():
    config = dict()
    config['pci_selector'] = [65, 491]
    config['epochs'] = {'image_model': 500, 'regular_model': 300, 'final_model': 300}
    config['conv_settings'] = {'layer1': 3, 'layer2': 300, 'layer4': 300}


    training_history = {'valLoss':[0.1, 0.1, 0.1]}
    exp = Experiment(training_history, config, 'debugging')
    print(exp.save())

if __name__ == "__main__":
    test()
