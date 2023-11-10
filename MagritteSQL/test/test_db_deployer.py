from unittest import TestCase

from lib.MagritteSQL.db_deployer import DbDeployer

class DbDeployerTest(TestCase):

    def test_deploy_table_unregistered_model(self):
        try:
            deployer = DbDeployer.create_db_deployer("sqlite://")
            deployer.deploy_table("person")
        except Exception as e:
            print(e)
            return
        assert False
