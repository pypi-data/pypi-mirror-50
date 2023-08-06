import os
import boto3
import mimetypes


class S3Service(object):

    def __init__(self,
            region_name,
            endpoint_url,
            aws_access_key_id,
            aws_secret_access_key):
        self.description = 'Amazon S3 or Amazon Simple Storage Service is\
a "simple storage service" offered by Amazon Web Services that provides object storage through a web service interface.'
        self.conn = boto3.resource('s3',
                        region_name=region_name,
                        endpoint_url=endpoint_url,
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key)

    def _upload_file_to_cloud(self,
            media_location,
            file_key,
            bucket,
            mime,
            guess_mime,
            acl):
        buck = self.conn.Bucket(bucket)
        file = open(media_location, 'rb')
        params = dict(
            Key=file_key,
            Body=file,
            ACL=acl)
        if mime:
            params['ContentType'] = mime
        elif guess_mime:
            guess_mime = mimetypes.guess_type(file)[0]
            if guess_mime:
                params['ContentType'] = guess_mime

        buck.put_object(**params)
        return '{}/{}/{}'.format(self.base_url, bucket, file_key)


    def _save_file_to_local(self,
            file,
            filename):
        media_location = '{}/{}'.format(os.getcwd(), filename)
        file.save(media_location)
        return media_location


    def _remove_file_from_local(self,
            media_location):
        os.remove(media_location)


    def _get_filename(self, file):
        *_, filename =  file.filename.split('/')
        return filename


    def upload_file(self,
            file,
            bucket,
            folder='',
            mime=None,
            guess_mime=False,
            acl='private'):
        filename = self._get_filename(file)
        file_key = filename
        if folder:
            file_key = '{}/{}'.format(folder, filename)
        media_location = self._save_file_to_local(file, filename)
        file_url = self._upload_file_to_cloud(
            media_location,
            file_key,
            bucket,
            mime,
            guess_mime,
            acl
        )
        self._remove_file_from_local(media_location)
        return file_url
