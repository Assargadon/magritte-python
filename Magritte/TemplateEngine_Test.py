
#import sys
#from pathlib import Path # if you haven't already done so
#file = Path(__file__).resolve()
#sys.path.append(str(file.parents[0]))
#sys.path.append(str(file.parents[1]))

# TODO - unit test

from model_for_tests.Host import Host
from model_for_tests.Port import Port
from accessors.MAAttrAccessor_class import MAAttrAccessor
from MAContainer_class import MAContainer
from MAStringDescription_class import MAStringDescription
from MAIntDescription_class import MAIntDescription
from MAToManyRelationDescription_class import MAToManyRelationDescription
from template_engine import MAModelCheetahTemplateAdapter


magritteModel = Host.random_host()

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

sTemplate = """
    Host IP: $magritteModel.ip
    #for $port in $magritteModel.ports
        Port Number: $port.numofport
    #end for
"""

adapter = MAModelCheetahTemplateAdapter(magritteModel, desc)
s = adapter.respondTo(sTemplate)
print(s)

#MAModelCheetahTemplateAdapter
