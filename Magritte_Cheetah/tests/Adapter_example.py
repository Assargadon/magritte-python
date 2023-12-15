import Cheetah.ErrorCatchers
import Cheetah.Template

# Do not forget add place with Magritte & Magritte_Cheetah to sys.path / PYTHONPATH
# i.e. `export PYTHONPATH="path to folder with folder Magritte inside"`

from Magritte.model_for_tests.Host import Host
from Magritte.model_for_tests.Port import Port
from Magritte.model_for_tests.EnvironmentProvider_test import TestEnvironmentProvider
from Magritte.model_for_tests.ModelDescriptor_test import TestModelDescriptor

from Magritte_Cheetah.MAModelCheetahTemplateAdapter import MAModelCheetahTemplateAdapter

environment = TestEnvironmentProvider()
hosts = environment.hosts #original, unadopted hosts
hostDescriptor = TestModelDescriptor.description_for("Host")
 
sTemplate = """
    We have ${len($hosts)} hosts totally:
    #for $host in $hosts
        =====================
        HOST $host.ip HAS ${len($host.ports)} ports:
        
        #for $port in $host.ports
            * $port.numofport
        #end for
        =====================
        
        
    #end for
"""

compiledTemplate = Cheetah.Template.Template(sTemplate)
compiledTemplate.hosts = [MAModelCheetahTemplateAdapter(host, hostDescriptor) for host in hosts] #Adopted hosts

print(compiledTemplate)
