#!python
from oss_api import *
import sys
import json
import os

def main():

    args = sys.argv[1:]

    if args[0] == "configure":
        c.main()
    else:
        if args[0] == "createScenario":
            cS.main()
        elif args[0] == "uploadLayer": 
            uL.main()
        else:
            print("%s is no valid option: choose between configure / createScenario / uploadLayer")

if __name__ == "__main__":
    import sys
    from optparse import OptionParser
    
    description = """oss [FUNCTION] [OPTIONS]
    
    FUNCTIONS:
     - configure:       Configure project and URL of the oss project
     - createScenario:  Create new scenario
     - uploadLayer:     Upload layer to a scenario
    """
    parser = OptionParser(description)

    args = sys.argv
    if not len(args)>1:
        parser.print_help()
    else:
        main()