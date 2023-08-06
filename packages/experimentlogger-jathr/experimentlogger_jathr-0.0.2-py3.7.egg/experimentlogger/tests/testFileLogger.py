from unittest import TestCase
import os
from experimentlogger import Experiment, load_experiment
from experimentlogger.utils.errors import CannotConnectMongoDB, ConfigNotDict
from pymongo.errors import ServerSelectionTimeoutError
import shutil

class TestBaseConstructor(TestCase):

    def setUp(self):
        self.config = dict()
        self.config['nn_layers'] = [30, 30, 30]
        self.exp = Experiment('file', config=self.config)
        self.exp.results = 'test_results'

    def test_config_error(self):
        self.assertRaises(ConfigNotDict, lambda:Experiment('file'))

    def test_config_dict(self):
        self.assertEqual(self.exp.config, self.config)

    def test_file_id_generator(self):
        self.assertIsNotNone(self.exp.id)

    def test_save_file(self):
        self.exp.save()
        self.assertTrue(os.path.isdir(self.exp.root_folder))
        self.assertTrue(os.path.isfile(self.exp.root_folder+'/'+self.exp.id+".json"))
        shutil.rmtree(self.exp.root_folder)

       

    def test_load_file(self):
        self.exp.save()
        self.assertTrue(os.path.isfile(self.exp.root_folder+'/'+self.exp.id+".json"))
        exp = load_experiment(self.exp.id)
        self.assertTrue(isinstance(exp, Experiment))
        self.assertEqual(self.exp.id, exp.id)
        self.assertEqual(self.exp.date,  exp.date)
        self.assertEqual(self.config['nn_layers'], exp.config['nn_layers'])
        shutil.rmtree(self.exp.root_folder)

        