from mongoengine import StringField, ReferenceField, DateTimeField, BinaryField
from .base import Base
from .report import ReportMongo


class OutputMongo(Base):
    __tablename__ = 'outputs'
    id = StringField(required=True)
    name = StringField()

    report = ReferenceField(ReportMongo)

    created = DateTimeField()
    data = BinaryField()

    def __repr__(self):
        return "<Output(name='%s')>" % (self.name)
