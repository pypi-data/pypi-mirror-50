import os
import glob
import requests
import json
import sys

from .authentication import tokenAuth
configurationPath = os.path.join(os.path.dirname(__file__), "ossConfig.json")

@tokenAuth
def uploadLayer(s, filename, name, group, sld, scenario):
    """Upload shapefile or geotiff layer to certain scenario
    
    Arguments:
        path {str} -- *.shp, *.nc or *.geotiff path
        name {str} -- Name for display in synapps
        group {str} -- Group for display in synapps
        sld {str} -- SLD name from geoserver
        scenario {int} -- scenario id
    """
    if os.path.exists(configurationPath):
        config = json.load(open(configurationPath, "r"))
        print("Uploading layer %s on project %s, scenario %s" % (name, config["project"], scenario))
    else:
        print("First define configuration using oss configure ...")
        sys.exit(2)

    rr = s.get(config["url"] + "/api/project/getscenarios/?project_id=%d"%config["project"])
    if rr.ok:
        scenarios = rr.json()["results"]
    else:
        if rr.status_code == 401:
            print("The service is requesting login information due to new security policy. Please use 'oss configure -U username -P password to set it up")
            return
        print("The project %d does not exist on %s" % (config["project"], config["url"]))
        sys.exit(2)
    
    if scenario not in map(lambda x: x["id"], scenarios):
        print("Scenario %d is no scenario of configured project %d" % (scenario, config["project"]))

    ls = glob.glob(os.path.splitext(filename)[0] + ".*")
    files = []
    for fileke in ls:
        rr = s.post(config["url"] + "/api/upload/", files={
            "files": (fileke, open(fileke, "rb"))
        })
        if rr.ok:
            files.append(rr.json()[0])
        else:
            print("File %s not accepted" % (fileke,))
    
    print("Files accepted: %s" % json.dumps(files))
    
    if not files:
        print("No single file was accepted: please try again")
        sys.exit(2)
    
    uploadedFiles = []
    for fileke in files:
        uploadedFiles.append({
            "id": fileke["fileName"],
            "filename": fileke["originalName"]
        })
    print(json.dumps(uploadedFiles))
    data = [{
        "active": False,
        "fileMapLayer": {
            "sld": sld,
            "uploadedFiles": uploadedFiles,
            "varname": "",
            "zoomStart": 9,
            "zoomStop": 20
        },
        "group": group,
        "legend_name": name,
        "wms_layer": "",
        "varname": "",
        "zindex": 1,
        "name": name,
        "folder": "",
        "time_dimension": False,
        "transparent": True,
        "wmsMapLayer": {"wms_layer": "","wms_url": ""},
        "uploadedFiles":uploadedFiles,
        "zoomStart": 9,
        "zoomStop": 20,
        "nc_file":"",
        "show": True,
        "showLayerAttributes": True,
        "sld": sld,
        "type": "map"
    }]
    rr = s.post(config["url"] + "/api/project/import_sublayer/?id=%d"%scenario, json=data)

    if not rr.ok:
        print(rr.text)
        print(rr.url)
        print(rr.data)
    else:
        print("ok: %s"% rr.json())

def main():
    import sys
    from optparse import OptionParser
    
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename", help="file for upload in synapps (*.shp, *.tif, *.nc)", metavar="FILE")
    parser.add_option("-n", "--name", dest="name", help="Name for display in synapps")
    parser.add_option("-s", "--sld", dest="sld", help="SLD name from geoserver")
    parser.add_option("-g", "--group", dest="group", help="group for display in synapps")
    parser.add_option("-i", "--id", dest="scenario", help="scenario id", type="int")
    
    s = requests.Session()
    (options, args) = parser.parse_args(sys.argv)
    if (not options.filename) or (not options.name) or (not options.sld) or (not options.group) or (not options.scenario):
        print("Not all arguments are given, all are required")
        parser.print_help()
    else:
        uploadLayer(s, **options.__dict__)

if __name__ == "__main__":
    main()