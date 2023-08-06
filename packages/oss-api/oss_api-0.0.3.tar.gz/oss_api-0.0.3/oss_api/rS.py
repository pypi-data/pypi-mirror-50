import os
import requests
import json
import sys

def removeScenario(id):
    """Create a scenario on an oss project.
    
    Arguments:
        config {dict} -- Project id (first request project id at synapps Admin)
        name {str} -- Name for display in Synapps
    """
    print("removeScenario not yet implemented")
    sys.exit(2)
    configurationPath = os.path.join(os.path.dirname(__file__), "ossConfig.json")
    if os.path.exists(configurationPath):
        config = json.load(open(configurationPath, "r"))
    else:
        print("First define configuration with oss configure ...")

    rr.get(config["url"] + "/api/project/getsimplelayers/?scenario_id=%d"%id)
    if rr.ok:
        layers = rr.json()
    if not layers:
        print("No layers: ok to remove scenario %d" % id)
        rr.delete("")
    else:
        print("Scenario is not empty! please remove layers first: %s" % json.dumps(layers))
    
def main():
    import sys
    from optparse import OptionParser
    
    print("Remove Scenario not yet implemented.")
    parser = OptionParser()
    parser.add_option("-i", "--id", dest="id", help="Scenario id to remove")
    (options, args) = parser.parse_args(sys.argv)
    
    if not options.id:
        print("-i / --id is required")
        parser.print_help()
    else:
        removeScenario(options.id)

if __name__ == "__main__":
    main()