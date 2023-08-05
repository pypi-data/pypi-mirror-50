class GenerateSchema():
    def __init__(self,resource_name, plural_name=None):
        self.resource_name = resource_name
        if not plural_name:
            self.plural_name = f'{self.resource_name}s'
        else:
            self.plural_name = plural_name

        self.model_name = self.resource_name.capitalize()
        self.schema_name = f'{self.resource_name.capitalize()}Schema'    
        
        self.opened_file = open(f'{resource_name}_schema.py',"a")

    def generate_imports(self):
        self.opened_file.write(f'from ma import ma')
        self.opened_file.write(f'\n')
        self.opened_file.write(f'from models.{self.resource_name} import {self.model_name}')
        self.opened_file.write(f'\n\n')

    def generate_schema_class(self):
        self.opened_file.write(f'class {self.schema_name}(ma.ModelSchema):')
        self.opened_file.write(f'\n\n\t')
        self.opened_file.write(f'class Meta:')
        self.opened_file.write(f'\n\t\t')
        self.opened_file.write(f'model = {self.model_name}')
        self.opened_file.write(f'\n\t\t')
        self.opened_file.write(f'include_fk = True')

    def generate(self):
        self.generate_imports()
        self.generate_schema_class()


        
        