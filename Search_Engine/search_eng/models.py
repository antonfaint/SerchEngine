from django.db import models
from django.utils.translation import ugettext_lazy as _
from any_urlfield.models import AnyUrlField
import pickle

class PickleField(models.TextField):
    __metaclass__ = models.SubfieldBase

    editable = False
    serialize = False

    def get_db_prep_value(self, value,connection,prepared):
        return pickle.dumps(value)

    def to_python(self, value):
        if not isinstance(value, basestring):
            return value

        # If not possible, return this value, cause it's not pickled yet.
        if isinstance(value, unicode):
            try:
                str_value = str(value)
            except UnicodeEncodeError:
                return value
        else:
            str_value = value

        try:
            return pickle.loads(str_value)
        except ValueError:

            # string saved to PickleField.
            return value

class Index_Model( models.Model ):

    index_url = AnyUrlField(_("URL"))
    index_data = PickleField()

# Create your models here.

