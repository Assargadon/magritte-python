
#import sys
#from pathlib import Path # if you haven't already done so
#file = Path(__file__).resolve()
#sys.path.append(str(file.parents[0]))
#sys.path.append(str(file.parents[1]))

# TODO - unit test

from unittest import TestCase

import Cheetah.ErrorCatchers
import Cheetah.Template

from model_for_tests.Host import Host
from model_for_tests.Port import Port
from accessors.MAAttrAccessor_class import MAAttrAccessor
from descriptions.MAContainer_class import MAContainer
from descriptions.MAStringDescription_class import MAStringDescription
from descriptions.MAIntDescription_class import MAIntDescription
from descriptions.MAToManyRelationDescription_class import MAToManyRelationDescription
from template_engine.MAModelCheetahTemplateAdapter_class import MAModelCheetahTemplateAdapter


class MADateDescriptionTest(TestCase):

    def setUp(self):
        self.magritteModel = Host.random_host()

        portDesc = MAContainer()
        portDesc += MAIntDescription(name='numofport', accessor=MAAttrAccessor('numofport'))

        desc = MAContainer()
        desc += MAStringDescription(name='ip', accessor=MAAttrAccessor('ip'))
        desc += MAToManyRelationDescription(
                name='ports',
                default=desc.defaultCollection(),
                classes=[Port],
                reference=portDesc,
                accessor=MAAttrAccessor('ports')
            )
        self.magritteDescription = desc
        self.adapter = MAModelCheetahTemplateAdapter(self.magritteModel, self.magritteDescription)


    def test_host_template(self):
        sTemplate = """
            Host IP: $adapter.ip
            #for $port in $adapter.ports
                Port Number: $port.numofport
            #end for
        """
        sHostResponse = f"Host IP: {self.magritteModel.ip}"
        sPortResponses = [f"Port Number: {port.numofport}" for port in self.magritteModel.ports]

        compiledTemplate = Cheetah.Template.Template(sTemplate, searchList=[self])
        response = compiledTemplate.respond()

        self.assertTrue(sHostResponse in response, "Host IP string must exist in template response")
        for sPortResponse in sPortResponses:
            self.assertTrue(sPortResponse in response, "Port Number string must exist in template response")


    def test_unexistent_property_template(self):
        sTemplate = """
            Host unexistent property: $magritteModel.unexistent
        """
        with self.assertRaises(Cheetah.ErrorCatchers.NotFound):
            compiledTemplate = Cheetah.Template.Template(sTemplate, searchList=[self])
            _ = compiledTemplate.respond()
