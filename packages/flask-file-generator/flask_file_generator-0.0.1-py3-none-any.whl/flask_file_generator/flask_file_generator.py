from generate_model import GenerateModel
from generate_resource import GenerateResource
from generate_schema import GenerateSchema


def generate_all(resource_name, plural_name=None):
    gen_model = GenerateModel(resource_name,plural_name)
    gen_model.generate()

    gen_schema = GenerateSchema(resource_name,plural_name)
    gen_schema.generate()

    gen_resource = GenerateResource(resource_name,plural_name)
    gen_resource.generate()


generate_all('event')