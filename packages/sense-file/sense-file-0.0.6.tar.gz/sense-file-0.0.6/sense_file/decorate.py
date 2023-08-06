import datetime
from sense_core import get_db_factory, DBACTION


def upload_db_logs(function):
    def inner(self, file_name, origin_path, bucket_name):
        _success, _msg = function(self, file_name, origin_path, bucket_name)
        if _success:
            key = file_name.split('/')[-1]
            db_factory = get_db_factory('mysql_file')
            _now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            _params = {'key': key, 'bucket_name': bucket_name,
                       'create_time': _now, 'modify_time': _now,
                       'status': 1}
            db_factory.findKeySql(DBACTION.REPLACE, table='file_sheet', data=_params)
        return _success, _msg
    return inner


def upload_pdf_logs(function):
    def inner(self, file_name, origin_path, bucket_name, publish_time=None, url=None, stock_code=None):
        _success, _msg = function(self, file_name, origin_path, bucket_name, publish_time, url, stock_code)
        if _success:
            key = file_name.split('/')[-1]
            db_factory = get_db_factory('mysql_file')
            _now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            _params = {'key': key, 'bucket_name': bucket_name,
                       'create_time': _now, 'modify_time': _now,
                       'status': 1, 'publish_time': publish_time,
                       'publish_day': publish_time, 'stock_code': stock_code, 'url': url}
            db_factory.findKeySql(DBACTION.REPLACE, table='pdfs_sheet', data=_params)
        return _success, _msg
    return inner


def upload_model_logs(function):
    def inner(self, file_name, origin_path, bucket_name, alg):
        _success, _msg = function(self, file_name, origin_path, bucket_name, alg)
        if _success:
            key = file_name.split('/')[-1]
            db_factory = get_db_factory('mysql_file')
            _now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            _params = {'key': key, 'bucket_name': bucket_name,
                       'create_time': _now, 'modify_time': _now,
                       'status': 1, 'alg': alg}
            db_factory.findKeySql(DBACTION.REPLACE, table='model_sheet', data=_params)
        return _success, _msg
    return inner


def delete_db_logs(function):
    def inner(self, file_name, bucket_name):
        _success, key = function(self, file_name, bucket_name)
        if _success:
            db_factory = get_db_factory('mysql_file')
            _now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db_factory.findKeySql(DBACTION.DELETE_BY_ATTR, table='file_sheet', params={'key': key})
        return _success, key

    return inner
