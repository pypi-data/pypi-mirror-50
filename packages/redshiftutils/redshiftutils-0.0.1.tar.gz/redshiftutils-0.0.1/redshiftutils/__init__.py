import boto3
import psycopg2


class RedshiftDataManager(object):

    def __init__(self, config):
        self.config = config

    def execute_update(self, con, cur, script):
        try:
            cur = con.cursor()
            cur.execute(script)
            cur.close()
            con.commit()
            result = True
        except Exception as ERROR:
            con.rollback()
            result = ERROR
        finally:
            if con is not None:
                con.close()
        return result

    def execute_query(self, con, cur, script):
        try:
            cur.execute(script)
            con.commit()
            result = cur.fetchall()
        except Exception as ERROR:
            con.rollback()
            result = ERROR
        finally:
            con.close()
        return result

    def get_conn(self):
        client = boto3.client('redshift')

        try:
            creds = client.get_cluster_credentials(
                DbUser=self.config['redshift_user'],
                DbName=self.config['redshift_database'],
                ClusterIdentifier=self.config['redshift_cluster'],
                DurationSeconds=3600)
        except Exception as ERROR:
            print(f"Credentials Issue: {ERROR}")

        try:
            conn = psycopg2.connect(
                dbname=self.config['redshift_database'],
                user=self.config['redshift_user'],
                password=self.config['redshift_password'],
                port=self.config['redshift_port'],
                host=self.config['redshift_endpoint'])

            return conn
        except Exception as ERROR:
            print(f"Connection Issue: {ERROR}")

    def run_update(self, script):
        return self.execute_update(
            RedshiftDataManager.get_conn(self),
            RedshiftDataManager.get_conn(self).cursor(),
            script)

    def run_query(self, script):
        return self.execute_query(
            self.get_conn(),
            self.get_conn().cursor(),
            script)