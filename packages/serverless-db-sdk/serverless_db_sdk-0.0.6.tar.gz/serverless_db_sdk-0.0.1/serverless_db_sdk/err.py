# -*- coding: utf8 -*-

DbNameErrContent = "The db name is empty or the environment variable DB_DEFAULT is empty"
EnvParamErrorContent = "The database connection parameter is not set in the environment variable"

ConnectErrorContent = "Database connection error, please verify that the set database environment variable " \
                      "is correct and the network can pass"
DatabaseErrorContent = "Database error"


class MySQLError(Exception):
    """Exception related to operation with MySQL."""


class Warning(Warning, MySQLError):
    """Exception raised for important warnings like data truncations
    while inserting, etc."""


class ParamError(Exception):
    """Exception that is the base class of all other error exceptions
    (not Warning)."""
