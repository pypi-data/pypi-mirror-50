
class GenerateResource():
    def __init__(self,resource_name, plural_name=None):
        self.resource_name = resource_name
        if not plural_name:
            self.plural_name = f'{self.resource_name}s'
        else:
            self.plural_name = plural_name

        self.model_name = self.resource_name.capitalize()
        self.schema_name = f'{self.resource_name.capitalize()}Schema'    
        
        self.opened_file = open(f'{resource_name}.py',"a")

    def generate_list_class(self):
        self.opened_file.write(f'class {self.resource_name.capitalize()}List(Resource):')
        self.opened_file.write(f'\n\t')
        self.opened_file.write(f'{self.resource_name}_schema = {self.schema_name}()')
        self.opened_file.write(f'\n')
        

    def generate_get_list(self):
        self.opened_file.write(f'\n\t')
        self.opened_file.write(f'def get(self):')
        self.opened_file.write(f'\n\t\t')
        self.opened_file.write(f'{self.plural_name} = {self.model_name}.query.all()')
        self.opened_file.write(f'\n\t\t')
        self.opened_file.write(f'return {{"data": {self.resource_name}_schema({self.plural_name}, many=True)}}')


    def generate_imports(self):
        self.opened_file.write(f'from flask_restful import Resource')
        self.opened_file.write(f'\n')
        self.opened_file.write(f'from models.{self.resource_name} import {self.model_name}')
        self.opened_file.write(f'\n')
        self.opened_file.write(f'from schemas.{self.resource_name} import {self.schema_name}')
        self.opened_file.write(f'\n')
        self.opened_file.write(f'from flask import request')
        self.opened_file.write(f'\n')
        self.opened_file.write(f'from db import db')
        self.opened_file.write(f'\n\n\n')

    def generate(self):
        self.generate_imports()
        self.generate_list_class()
        self.generate_get_list()
        
