from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):
    """
    class to create a custom model field. This field will be used
    to order objects. The order will be relative to other objects.
    Modules in a course will be ordered with respect to the course
    that they belong to. Content of a module will be ordered with respect
    to the module they belong to.
    In this class for_field represent either a course or a module.
    """
    def __init__(self, for_fields=None, *args, **kwargs):
        """

        :param for_fields:
        :param args:
        :param kwargs:
        """
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        """
        Overriding the method inherited from PositiveIntegerField.
        This method is executed before data is saved to the database.
        :param model_instance:
        :param add:
        :return:
        """
        # We check if a value has already been given to the OrderField
        # in the model instance.
        # getattr takes multiple parameters, the object whose attribute value
        # is to be found, the string that contains the attribute name, an optional
        # default value that is returned when the named attribute is not found.
        # If no default is provided and attribute doesn't exist an AttributeError is thrown.
        if getattr(model_instance, self.attname) is None:
            # no current value
            try:
                qs = self.model.objects.all()
                if self.for_fields:
                    # filter by objects with the same field values
                    # for the fields in 'for_fields'
                    query = {field: getattr(model_instance, field) for field in self.for_fields}
                    qs = qs.filter(**query)
                # get the order of the last item
                last_item = qs.latest(self.attname)
                value = last_item.order +1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)
