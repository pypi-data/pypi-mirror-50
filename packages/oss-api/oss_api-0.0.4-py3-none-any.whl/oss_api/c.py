import os
import json

configurationPath = os.path.join(os.path.dirname(__file__), "ossConfig.json")

def main():
    import sys
    from optparse import OptionParser

    description = "oss configure [OPTIONS]"

    parser = OptionParser(description)
    parser.add_option("-p", "--project", dest="project", help="Project id in oss", type="int")
    parser.add_option("-u", "--url", dest="url", default="https://oss.imdcapps.be", help="""URL for oss (default: {"https://oss.imdcapps.be"})""")
    parser.add_option("-U", "--username", dest="username", help="Username in CAS")
    parser.add_option("-P", "--password", dest="password", help="Password in CAS")

    (options, args) = parser.parse_args(sys.argv)
    if os.path.exists(configurationPath):
        print("old config is : %s" % json.dumps(json.load(open(configurationPath, "r"))))
    configure(**options.__dict__)
    
    print("new config is : %s" % json.dumps(json.load(open(configurationPath, "r"))))

def configure(**kwargs):
    """Set the configuration for this api, meaning oss url and project id
    
    Arguments:
        project {int} -- Project id in oss
    
    Keyword Arguments:
        url {str} -- URL for oss (default: {"https://oss.imdcapps.be"})
    
    Returns:
        dict -- Configuration object
    """
    try:
        config = json.load(open(configurationPath, "r"))        
    except:
        config =  {
            # "project": project,
            # "url": url
        }
    kwargs = {k:v for (k,v) in kwargs.iteritems() if v}
    print(kwargs)
    config.update(kwargs)

    if not "project" in config:
        print("-p/ --project option is required")
        return 

    try:
        json.dump(config, open(configurationPath, "w"))
    except Exception as e:
        raise RuntimeError(e)
    return config

if __name__ == "__main__":
    main()