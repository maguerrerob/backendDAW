from import_export import resources
from .models import *

class ProductoResource(resources.ModelResource):
    class Meta:
        model = Producto
        import_id_fields = ['nombre']
        skip_unchanged = True
        use_bulk = True