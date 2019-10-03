from mongoengine import BooleanField, StringField, ReferenceField, DateTimeField, CASCADE
from paperboy.config import ReportConfig, ReportMetadataConfig
from .base import Base
from .user import UserMongo


class ReportMongo(Base):
    __tablename__ = 'reports'
    name = StringField()

    user = ReferenceField(UserMongo)
    notebook = ReferenceField('NotebookMongo', reverse_delete_rule=CASCADE)
    job = ReferenceField('JobMongo', reverse_delete_rule=CASCADE)

    parameters = StringField()
    type = StringField()
    output = StringField()
    strip_code = BooleanField()

    created = DateTimeField()
    modified = DateTimeField()

    @staticmethod
    def from_config(rp):
        # FIXME
        return ReportMongo(name=rp.name,
                           user=rp.user,
                           notebook=rp.notebook,
                           job=rp.job,
                           parameters=rp.meta.parameters,
                           type=rp.meta.type,
                           output=rp.meta.output,
                           strip_code=rp.meta.strip_code,
                           created=rp.meta.created,
                           modified=rp.meta.modified)

    def to_config(self, config):
        ret = ReportConfig(config)
        ret.id = 'Report-' + str(self.id)
        ret.name = self.name

        meta = ReportMetadataConfig()
        meta.notebook = self.notebook.to_config(config)
        meta.job = self.job.to_config(config)
        meta.username = self.user.name
        meta.userid = 'User-' + str(self.user.id)

        meta.parameters = self.parameters
        meta.type = self.type
        meta.output = self.output
        meta.strip_code = self.strip_code

        # meta.template = self.template  # FIXME implement
        meta.created = self.created
        meta.modified = self.modified
        ret.meta = meta
        return ret

    def __repr__(self):
        return "<Report(name='%s')>" % (self.name)
