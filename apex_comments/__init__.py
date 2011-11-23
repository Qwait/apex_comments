from sqlalchemy import engine_from_config

from apex_comments.models import initialize_sql


def includeme(config):
    settings = config.registry.settings
    
    initialize_sql(engine_from_config(settings, 'sqlalchemy.'))