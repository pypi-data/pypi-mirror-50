import os
from boto3.session import Session
from sense_core import config, log_error
from sense_file.decorate import delete_db_logs, upload_db_logs, upload_pdf_logs, upload_model_logs


class S3File(object):

    def __init__(self, label, region_name='cn-north-1'):
        _key, _secret = os.getenv('S3_KEY', None), os.getenv('S3_SECRET', None)
        if not _key:
            _key, _secret = config(label, 'key'), config(label, 'secret')
        session = Session(aws_access_key_id=_key, aws_secret_access_key=_secret,
                          region_name=region_name)
        self.session = session
        self.server = session.resource('s3')
        self.client = None
        self.bucket_map = {}

    def __get_client(self):
        if not self.client:
            self.client = self.session.client('s3')
        return self.client

    def __file_key_format(self, file_name):
        file_list = file_name.split('.')
        file_type = file_list[-1]
        file_list[-1] = file_type.lower()
        return '.'.join(file_list)

    def __get_bucket(self, bucket_name):
        if bucket_name not in self.bucket_map:
            self.bucket_map[bucket_name] = self.server.Bucket(bucket_name)
        return self.bucket_map[bucket_name]

    def file_exists(self, file_name, bucket_name):
        bucket = self.__get_bucket(bucket_name)
        for obj in bucket.objects.filter(Prefix=file_name):
            if obj.key == file_name:
                return True
        return False

    def download(self, file_name, aim_path, bucket_name):
        """
        下载文件接口
        :param file_name:
        :param aim_path:
        :param bucket_name:
        :return:
        """
        file_name = self.__file_key_format(file_name)
        if not self.file_exists(file_name, bucket_name):
            return False, 'file not exists'
        try:
            self.server.Object(bucket_name, file_name).download_file(aim_path)
        except Exception as e:
            log_error(
                'file {} down from s3 {} error,msg: {}'.format(file_name, bucket_name, e.__str__()))
            return False, 'down error {}'.format(e.__str__())
        return os.path.exists(aim_path), file_name

    def __s3_upload_file(self, bucket_name, file_name, origin_path):
        _msg = '{}-{} upload file success '.format(file_name, bucket_name)
        try:
            obj = self.server.Object(bucket_name, file_name)
            obj.upload_file(origin_path)
        except Exception as ex:
            _msg = 'file {} upload from s3 {} error,msg: {}'.format(file_name, bucket_name,
                                                                    ex.__str__())
            log_error(_msg)
            return False, _msg
        return True, _msg

    @upload_pdf_logs
    def upload_pdf(self, file_name, origin_path, bucket_name, publish_time=None, url=None, stock_code=None):
        """ 上传公告，并写日志
        :param file_name: 文件名称
        :param origin_path: 源路径（本地路径）
        :param bucket_name:  aws s3桶
        :param publish_time,stock_code,url 装饰器使用字段来记录日志中
        :return:
        """
        file_name = self.__file_key_format(file_name)
        code, msg = self.__s3_upload_file(bucket_name, file_name, origin_path)
        return self.file_exists(file_name, bucket_name), msg

    @upload_model_logs
    def upload_model(self, file_name, origin_path, bucket_name, alg):
        """ 上传模型文件或配置，并写日志
        :param file_name: 文件名称
        :param origin_path: 源路径（本地路径）
        :param bucket_name:  aws s3桶
        :return:
        """
        code, msg = self.__s3_upload_file(bucket_name, file_name, origin_path)
        return self.file_exists(file_name, bucket_name), msg

    @upload_db_logs
    def upload(self, file_name, origin_path, bucket_name):
        """ 上传文件
        :param file_name: 文件名称
        :param origin_path: 源路径（本地路径）
        :param bucket_name:  aws s3桶
        :return:
        """
        file_name = self.__file_key_format(file_name)
        code, msg = self.__s3_upload_file(bucket_name, file_name, origin_path)
        return self.file_exists(file_name, bucket_name), msg

    @delete_db_logs
    def delete_file(self, file_name, bucket_name):
        file_name = self.__file_key_format(file_name)
        try:
            file_obj = self.server.Object(bucket_name, file_name)
            res = file_obj.delete()
        except Exception as e:
            log_error('file {} delete from s3 {} error,msg: {}'.format(file_name, bucket_name,
                                                                       e.__str__()))
            return False, 'delete error {}'.format(e.__str__())
        return True, file_name

    @upload_db_logs
    def upload_content(self, file_name, content, bucket_name, publish_time=None):
        file_name = self.__file_key_format(file_name)
        try:
            client = self.__get_client()
            client.put_object(Bucket=bucket_name, Key=file_name,
                              Body=bytes(content, encoding='utf-8'))
        except Exception as e:
            log_error('file {} upload from s3 {} error,msg: {}'.format(file_name, bucket_name,
                                                                       e.__str__()))
            return False, 'upload content error {}'.format(e.__str__())
        return self.file_exists(file_name, bucket_name), file_name


if __name__ == '__main__':
    s3_file = S3File('aws')
    _path = '/Users/liuguangbin/Documents/alg/conf/news_post_v2019081215.ini'
    # print(s3_file.download('tttt.txt', '/Users/liuguangbin/Documents/ttttt.txt',
    #                        'sdai-txt'))
    # print(s3_file.delete_file('tttt.txt', 'sdai-txt'))
    # x = s3_file.file_exists('000b9ccb-76d7-5421-997d-e3b8413479a2', 'sdai-pdfs')
    # print(s3_file.upload('000b9ccb-76d7-5421-997d-e3b8413479a2.PDF', file_path, 'sdai-pdfs'))
