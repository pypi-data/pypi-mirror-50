"""
    Persistence Adaptor Module
"""
from Audit.common import AppConfigurations
from Audit.core.persistences.adaptors import CassandraPersistenceAdaptor

#  Register New Adaptors Here
all_registered_adaptors = {"cassandra_persistence_adaptor": CassandraPersistenceAdaptor}


def get_instance(app_module):
    """
    This method the instance of the app module from the corresponding registered adaptor
    :param app_module:
    :return:
    """
    if AppConfigurations.persistence_adaptor not in all_registered_adaptors:
        raise Exception("No registered persistence Adaptor for {}".format(AppConfigurations.persistence_adaptor))
    given_adaptor = all_registered_adaptors[AppConfigurations.persistence_adaptor]
    return getattr(given_adaptor, app_module)()