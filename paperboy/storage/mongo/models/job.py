from mongoengine import StringField, ReferenceField, DateTimeField, ListField, CASCADE
from paperboy.config import JobConfig, JobMetadataConfig
from .base import Base
from .user import UserMongo


class JobMongo(Base):
    name = StringField()
    user = ReferenceField(UserMongo, reverse_delete_rule=CASCADE)
    notebook = ReferenceField('NotebookMongo', reverse_delete_rule=CASCADE)
    reports = ListField(ReferenceField('ReportMongo'))

    start_time = DateTimeField()
    interval = StringField()
    level = StringField()

    created = DateTimeField()
    modified = DateTimeField()

    @staticmethod
    def from_config(jb):
        # FIXME
        return JobMongo(name=jb.name,
                        user=jb.user,
                        notebook=jb.notebook,
                        reports=jb.meta.reports,
                        start_time=jb.meta.start_time,
                        interval=jb.meta.interval,
                        level=jb.meta.level,
                        created=jb.meta.created,
                        modified=jb.meta.modified)

    def to_config(self, config):
        ret = JobConfig(config)
        ret.id = 'Job-' + str(self.id)
        ret.name = self.name

        meta = JobMetadataConfig()
        meta.notebook = self.notebook.to_config(config)
        meta.username = self.user.name
        meta.userid = 'User-' + str(self.user.id)

        meta.start_time = self.start_time
        meta.interval = self.interval
        meta.level = self.level

        meta.reports = len(self.reports)

        meta.created = self.created
        meta.modified = self.modified

        ret.meta = meta
        return ret

    def __repr__(self):
        return "<Job(name='{}', user='{}', notebook='{}', start='{}', interval='{}'>".format(self.name, self.user, self.notebook, self.start_time, self.interval)
