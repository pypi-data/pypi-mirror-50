import random
from datetime import timedelta
from decimal import Decimal

from django.db import models
from django.utils.timezone import now
from faker import Faker

fake = Faker()

class ModelFactory:
    model = None
    fields = '__all__'  # which fields will be not null, ie. randomly generated or randomly chosen from db
    exclude = []  # which fields has to remain null
    random_fk_fields = []  # which related fields will be randomly chosen (otherwise generated)
    initial = {}
    related_factories = {}

    def __init__(self, model, fields='__all__', exclude=None, initial=None, random_fk_fields=None,
                 related_factories=None, use_defaults=True):

        if random_fk_fields is None:
            random_fk_fields = []

        if initial is None:
            initial = {}

        if exclude is None:
            exclude = []

        if related_factories is None:
            related_factories = {}

        self.model = model
        self.fields = fields
        self.exclude = exclude
        self.initial = initial
        self.random_fk_fields = random_fk_fields
        self.related_factories = related_factories
        self.use_defaults = use_defaults

    def create_base(self):
        return self.model.objects.create()

    def checkfield__is_excluded(self, field):
        return field.name in self.exclude

    def checkfield__in_fields(self, field):
        return self.fields == '__all__' or field.name in self.fields

    def checkfield__has_default(self, field):
        return field.default != models.fields.NOT_PROVIDED

    def create(self):
        obj = self.model()

        for field in obj._meta.fields:
            if self.checkfield__is_excluded(field):
                continue

            if not self.checkfield__in_fields(field):
                continue

            if self.use_defaults:  # will be automatically filled before save()
                if self.checkfield__has_default(field):
                    continue

            if field.name in self.initial.keys():
                setattr(obj, field.name, self.initial[field.name])
                continue

            if field.choices:
                random_choice = random.choice(field.choices)
                setattr(obj, field.name, random_choice[0])
                continue

            if isinstance(field, models.CharField):
                setattr(obj, field.name, self.gen_for_charfield())
            elif isinstance(field, models.TextField):
                setattr(obj, field.name, self.gen_for_textfield())
            elif isinstance(field, models.IntegerField):
                setattr(obj, field.name, self.gen_for_integerfield())
            elif isinstance(field, models.DecimalField):
                setattr(obj, field.name, self.gen_for_decimalfield())
            elif isinstance(field, models.DateField):
                setattr(obj, field.name, now().date() + timedelta(days=random.choice(range(-100, 100))))
            elif isinstance(field, models.DateTimeField):
                setattr(obj, field.name, now() + timedelta(hours=random.choice(-24 * 100, 24 * 100)))
            elif isinstance(field, models.BooleanField) or isinstance(field, models.NullBooleanField):
                setattr(obj, field.name, random.choice([False, True]))
            elif isinstance(field, models.ForeignKey) or isinstance(field, models.OneToOneField):
                Model = field.related_model
                if field.name in self.random_fk_fields:
                    setattr(obj, field.name, self.get_random_object(Model))
                else:
                    if field.name in self.related_factories.keys():
                        modelfactory = self.related_factories[field.name]
                        setattr(obj, field.name, self.gen_for_foreignkey(modelfactory=modelfactory))
                    else:
                        setattr(obj, field.name, self.gen_for_foreignkey(modelclass=Model))
        print(obj.__dict__)
        obj.save()
        return obj

    @classmethod
    def get_random_object(cls, Model):
        count = Model.objects.count()
        return Model.objects.all()[random.choice(range(0, count))]

    @classmethod
    def gen_for_charfield(cls):
        return fake.word()

    @classmethod
    def gen_for_textfield(cls):
        return fake.text()

    @classmethod
    def gen_for_integerfield(cls):
        return random.randint(1, 1000000)

    @classmethod
    def gen_for_decimalfield(cls):
        return Decimal(cls.gen_for_integerfield())

    @classmethod
    def gen_for_foreignkey(cls, modelclass=None, modelfactory=None):
        if not modelclass and not modelfactory:
            raise Exception("Either modelclass XOR modelfactory must not be None...")
        if modelfactory:
            obj = modelfactory.create()
        else:
            Factory = ModelFactory(model=modelclass)
            obj = Factory.create()
        return obj