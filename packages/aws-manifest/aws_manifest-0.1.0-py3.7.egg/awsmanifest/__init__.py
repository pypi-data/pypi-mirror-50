import json
import os

import requests

pkg_dir, _ = os.path.split(__file__)
local_policy_doc = f"{pkg_dir}/policies.js"
policies_url = "https://awspolicygen.s3.amazonaws.com/js/policies.js"

def remote_manifest(url: str = policies_url) -> str:
    """
    Retrieve the latest manifest containing AWS services and actions
    """
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text

def local_manifest(filename: str = local_policy_doc) -> str:
    """
    Retrieve the manifest bundled with the package
    """
    with open(local_policy_doc, "r") as f:
        return f.read()

def manifest(local: bool = False) -> dict:
    """
    Return a dictionary containing a mapping from amazon services
    to their actions
    """
    return AwsManifest(local).raw

class AwsManifest:
    """
    A class for retrieving information about aws resources and their actions.

    self.raw contains a dict with the full aws policy document
    self.service_map contains a dict with aws resources and actions
    """
    def __init__(self, local: bool = False):
        self.doc = local_manifest() if local else remote_manifest()

        # The manifest is a javascript file that defines a js object
        # Find the start of the object ("{"), and convert to a dict.
        idx = self.doc.find("{")
        self.raw = json.loads(self.doc[idx:])
        self.service_map = self.raw["serviceMap"]

    def services(self) -> list:
        """
        Return a list containing the full names of aws services
        """
        return self.service_map.keys()

    def service_prefixes(self) -> list:
        """
        Return a list containing the prefix names for aws services
        """
        return [self.service_map[svc]["StringPrefix"] for svc in self.service_map.keys()]

    def actions(self, svc: str) -> list:
        """
        Return a list of actions for a given service.
        Full service names ("Amazon Ec2") or service prefixes ("ec2") are
        accepted.
        """
        for k, v in self.service_map.items():
            if svc == k or svc == v["StringPrefix"]:
                return v["Actions"]
        raise KeyError(svc)
