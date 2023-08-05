class GenerateModel():
    def __init__(self,resource_name, plural_name=None):
        self.resource_name = resource_name
        if not plural_name:
            self.plural_name = f'{self.resource_name}s'
        else:
            self.plural_name = plural_name

        self.model_name = self.resource_name.capitalize()
        self.schema_name = f'{self.resource_name.capitalize()}Schema'    
        
        self.opened_file = open(f'{resource_name}_model.py',"a")

    def generate_imports(self):
        self.opened_file.write(f'from db import db')
        self.opened_file.write(f'\n\n')


    def generate_model_class(self):
        self.opened_file.write(f'class {self.model_name}(db.Model):')
        self.opened_file.write(f'\n\t')
        self.opened_file.write(f'__tablename__ = "{self.plural_name}"')
        self.opened_file.write(f'\n\n\t')
        self.opened_file.write(f'id = db.Column(db.Integer, primary_key=True)')

    def generate(self):
        self.generate_imports()
        self.generate_model_class()
