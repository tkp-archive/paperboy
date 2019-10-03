from mongoengine import ListField, StringField, ReferenceField
from .base import Base


class UserMongo(Base):
    __tablename__ = 'users'
    name = StringField(required=True)
    password = StringField(default='')

    notebooks = ListField(ReferenceField('NotebookMongo'))
    jobs = ListField(ReferenceField('JobMongo'))
    reports = ListField(ReferenceField('ReportMongo'))

    def __repr__(self):
        return "<User(name='%s')>" % self.name
