from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Brand, Category

@registry.register_document
class BrandDocument(Document):
    category = fields.NestedField(properties={'name': fields.TextField()})

    class Index:
        name = 'brands'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Brand
        fields = [
            'name',
            'slug',
            'description'
        ]
        #related_models = [Category]
