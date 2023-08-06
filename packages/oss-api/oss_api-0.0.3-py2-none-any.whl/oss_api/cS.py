import os
import requests
import json

from .authentication import tokenAuth

@tokenAuth
def createScenario(s, name):
    """Create a scenario on an oss project.
    
    Arguments:
        config {dict} -- Project id (first request project id at synapps Admin)
        name {str} -- Name for display in Synapps
    """
    configurationPath = os.path.join(os.path.dirname(__file__), "ossConfig.json")
    if os.path.exists(configurationPath):
        config = json.load(open(configurationPath, "r"))
        print("Creating scenario %s on project %d" % (name, config["project"]))
    else:
        print("First define configuration with oss configure ...")
    
    scenario_id = 1
    rr = s.post(config["url"] + "/api/project/create_update_scenario/?project_id=%d"%config["project"], {
        "name": name,
        "description": name,
        "projectId": config["project"],
        "attribute": ""
    })
    if rr.ok: 
        print("Scenario_id = %d" % rr.json()["id"])
        return rr.json()["id"]
    else:
        if rr.status_code == 401:
            print("The service is requesting login information due to new security policy. Please use 'oss configure -U username -P password to set it up")
            return
        print(rr.text)
        return rr.text

def main():
    import sys
    from optparse import OptionParser
    
    parser = OptionParser()
    parser.add_option("-n", "--name", dest="name", help="Scenario name for display in synapps")
    (options, args) = parser.parse_args(sys.argv)
    
    s = requests.Session()
    if not options.name:
        print("-n / --name is required")
        parser.print_help()
    else:
        createScenario(s, options.name)

if __name__ == "__main__":
    main()