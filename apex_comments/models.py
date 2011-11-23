from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy import types
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import func

from zope.sqlalchemy import ZopeTransactionExtension 

from apex.models import AuthUser

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Comment(Base):
    """ Comment Base.
    """
    __tablename__ = 'apex_comments'
    __table_args__ = {'sqlite_autoincrement': True}
 
    id = Column(types.Integer, primary_key=True)
    user_id = Column(types.Integer, ForeignKey(AuthUser.id), index=True)
    submit_date = Column(types.DateTime, default=func.now())
    comment = Column(types.Text)

    user = relationship(AuthUser, uselist=False)

class Commentable(object):
    """ Commentable mixin.
    """
    @declared_attr
    def comments(cls):
        comment_association = Table('%s_comments' % cls.__tablename__, cls.metadata,
            Column('comment_id', ForeignKey('apex_comments.id', onupdate='CASCADE', ondelete='CASCADE')),
            Column('%s_id' % cls.__tablename__, ForeignKey('%s.id' % cls.__tablename__, onupdate='CASCADE', ondelete='CASCADE')),
        )
        return relationship(Comment, secondary=comment_association)


def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
