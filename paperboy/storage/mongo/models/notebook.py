from mongoengine import IntField, StringField, ReferenceField, DateTimeField, ListField
from paperboy.config import NotebookConfig, NotebookMetadataConfig
from .base import Base
from .user import UserMongo


class NotebookMongo(Base):
    __tablename__ = 'notebooks'
    id = IntField(required=True)
    name = StringField()

    user = ReferenceField(UserMongo)
    jobs = ListField(ReferenceField('JobMongo'))
    reports = ListField(ReferenceField('ReportMongo'))

    notebook = StringField()
    privacy = StringField()
    level = StringField()
    requirements = StringField()
    dockerfile = StringField()

    created = DateTimeField()
    modified = DateTimeField()

    @staticmethod
    def from_config(nb):
        # FIXME
        return NotebookMongo(name=nb.name,
                             user=nb.user,
                             notebook=nb.notebook,
                             privacy=nb.meta.privacy,
                             level=nb.meta.level,
                             requirements=nb.meta.requirements,
                             dockerfile=nb.meta.dockerfile,
                             created=nb.meta.created,
                             modified=nb.meta.modified)

    def to_config(self, config):
        ret = NotebookConfig(config)
        ret.id = 'Notebook-' + str(self.id)
        ret.name = self.name

        meta = NotebookMetadataConfig()

        meta.username = self.user.name
        meta.userid = 'User-' + str(self.user.id)

        meta.notebook = self.notebook
        meta.privacy = self.privacy
        meta.level = self.level

        meta.requirements = self.requirements
        meta.dockerfile = self.dockerfile

        meta.jobs = len(self.jobs)
        meta.reports = len(self.reports)

        meta.created = self.created
        meta.modified = self.modified

        ret.meta = meta
        return ret

    def __repr__(self):
        return "<Notebook(name='{}', user='{}', privacy='{}', level='{}'>".format(self.name, self.user, self.privacy, self.level)
