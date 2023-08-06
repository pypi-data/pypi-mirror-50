import os
import requests
import json


def createScenario(name):
    """Create a scenario on an oss project.
    
    Arguments:
        config {dict} -- Project id (first request project id at synapps Admin)
        name {str} -- Name for display in Synapps
    """
    configurationPath = os.path.join(os.path.dirname(__file__), "ossConfig.json")
    if os.path.exists(configurationPath):
        config = json.load(open(configurationPath, "r"))
    else:
        print("First define configuration with oss configure ...")
    
    scenario_id = 1
    rr = requests.post(config["url"] + "/api/project/create_update_scenario/?project_id=%d"%config["project"], {
        "name": name,
        "description": name,
        "projectId": config["project"],
        "attribute": ""
    })
    if rr.ok: 
        print("Scenario_id = %d" % rr.json()["id"])
        return rr.json()["id"]
    else:
        return rr.text

def main():
    import sys
    from optparse import OptionParser
    
    print("Remove layer not yet implemented")
    parser = OptionParser()
    parser.add_option("-n", "--name", dest="name", help="Scenario name for display in synapps")
    (options, args) = parser.parse_args(sys.argv)
    
    if not options.name:
        print("-n / --name is required")
        parser.print_help()
    else:
        createScenario(options.name)

if __name__ == "__main__":
    main()