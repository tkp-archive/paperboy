from mongoengine import IntField, StringField, ReferenceField, DateTimeField, BinaryField
from .base import Base
from .report import ReportMongo


class OutputMongo(Base):
    __tablename__ = 'outputs'
    id = IntField(required=True)
    name = StringField()

    report = ReferenceField(ReportMongo)

    created = DateTimeField()
    data = BinaryField()

    def __repr__(self):
        return "<Output(name='%s')>" % (self.name)
