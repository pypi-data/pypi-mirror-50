"""Auto-generated module for the datacustodian package that creates a customized
component for a flask app.
"""
import sys
import logging
from flask import Blueprint, request
from flask_restplus import Resource
from datacustodian.utility import import_fqn
from datacustodian.api import create_parsers, Schema, apis
from datacustodian.settings import specs

log = logging.getLogger(__name__)

blueprint = Blueprint('ipfs',
                      'clearshare.ipfs',
                      url_prefix='/ipfs')
"""Blueprint: component-level modularization of component for a global flask app.
"""
api = apis["ipfs"]
"""flask_restplus.Api: api object to handle the blueprint for this component.
"""
api.init_app(blueprint)

model_specs = specs["ipfs"]["models"]
"""list: of model spec `dict` instances with raw model schemas"""
models = Schema()
"""Schema: model schema definitions for the component.
"""
models.load("ipfs", model_specs)

parsers = create_parsers(specs["ipfs"].parsers)
"""dict: keys are parser names, values are :class:`flask_restplus.RequestParser`.
"""

ns_specs = specs["ipfs"].namespaces
"""dict: keys are namespace names; values are the raw specification `dict` for
that namespace.
"""
namespaces = {}
"""dict: keys are namespace names, values are :class:`flask_restplus.Namespace`
objects.
"""
for nspec in ns_specs:
    namespaces[nspec.name] = api.namespace(nspec.name)

ns_data = namespaces["data"]

#Reinitialize the keyword arguments for the namespace; these just affect
#attributes on the namespace object, which will retain its pointer.
_nspeclookup = {s.name: s for s in ns_specs}
for nsname, ns in namespaces.items():
    nspec = _nspeclookup[nsname]
    ns.description = nspec.get("description", None)
    ns._path = nspec.get("path", None)
    ns._validate = nspec.get("validate", None)
    ns.decorators = nspec.get("decorators", [])
    ns.authorizations = nspec.get("authorizations", None)
    ns.ordered = nspec.get("ordered", False)

def _get_expectant(name):
    """Returns a parser with the given name, if it exists. If it doesn't,
    attempts to get a *model* with that name. If no model exists, an error
    is raised.
    """
    return parsers.get(name, models.get(name))


@ns_data.route(*['/browse/<path:reqpath>'])
class Browse(Resource):
    @api.expect(_get_expectant("Pagination"),
                validate=False)
    @api.marshal_with(models["DirectoryLs"],
                      skip_none=False)
    def post(ns, *args, **kwargs):
        """Get the contents of `req_path` in the local cluster storage. If it is a folder, list its contents; otherwise return the contents of the file.

        """
        if "Pagination" in parsers:
            kwargs = parsers["Pagination"].parse_args(request)
        kwargs["_data"] = request.json
        kwargs["_request"] = request

        mod, call = import_fqn("datacustodian.ipfs.dirlist")
        results = call(*args, **kwargs)
        return results
    

@ns_data.route(*['/download/<path:reqpath>'])
class Download(Resource):
    def get(ns, *args, **kwargs):
        """Download the contents of the specified file, which is assumed to be in local server storage. The first part of the `reqpath` should be a valid, configured root directory in the configuration files.

        """
        kwargs.update({})
        kwargs["_data"] = request.json
        kwargs["_request"] = request

        mod, call = import_fqn("datacustodian.ipfs.download")
        results = call(*args, **kwargs)
        return results
    

@ns_data.route(*['/files/<string:reqpath>', '/files/<path:reqpath>'])
class Files(Resource):
    @api.marshal_with(models["IPFSAddResult"],
                      skip_none=False)
    @api.response(200, "File added (and pinned) successfully.")
    def post(ns, *args, **kwargs):
        """Add the file included in the POST to the IPFS cluster. This operation *also* pins the file to the local node.

        """
        kwargs.update({})
        kwargs["_data"] = request.json
        kwargs["_request"] = request

        mod, call = import_fqn("datacustodian.ipfs.add")
        results = call(*args, **kwargs)
        return results, 200
        
    
    @api.marshal_with(models["IPFSAddResult"],
                      skip_none=False)
    @api.response(200, "File added (and pinned) successfully.")
    def put(ns, *args, **kwargs):
        """Add the *local* file included in the PUT request path to the IPFS cluster. This operation *also* pins the file to the local node.

        """
        kwargs.update({})
        kwargs["_data"] = request.json
        kwargs["_request"] = request

        mod, call = import_fqn("datacustodian.ipfs.add_local")
        results = call(*args, **kwargs)
        return results, 200
        
    
    def get(ns, *args, **kwargs):
        """Download the specified file from the IPFS cluster. If the file is not pinned on the local node, it will be retrieved from the IPFS network.

        """
        kwargs.update({})
        kwargs["_data"] = request.json
        kwargs["_request"] = request

        mod, call = import_fqn("datacustodian.ipfs.get")
        results = call(*args, **kwargs)
        return results
    
    @api.marshal_with(models["IPFSUnpinResult"],
                      skip_none=False)
    @api.response(200, "File unpinned successfully.")
    def delete(ns, *args, **kwargs):
        """Remove the specified file from the IPFS cluster. Note that IPFS is the *permanent* web, so things never get deleted from IPFS itself. However, you can choose to not pin things anymore so that they are deleted locally. If nobody is pinning something, it is essentially deleted since a lookup will not return any peers that can actually serve the content.

        """
        kwargs.update({})
        kwargs["_data"] = request.json
        kwargs["_request"] = request

        mod, call = import_fqn("datacustodian.ipfs.rm")
        results = call(*args, **kwargs)
        return results, 200
        
    

@ns_data.route(*['/pins/<string:reqpath>'])
class Pins(Resource):
    @api.response(200, "File pinned successfully.")
    def put(ns, *args, **kwargs):
        """Pin the specified IPFS address to the local node. This makes the node download the file from the IPFS network so that it has a local copy.

        """
        kwargs.update({})
        kwargs["_data"] = request.json
        kwargs["_request"] = request

        mod, call = import_fqn("datacustodian.ipfs.pin")
        results = call(*args, **kwargs)
        return results, 200
        
    
    @api.marshal_with(models["IPFSUnpinResult"],
                      skip_none=False)
    @api.response(200, "File unpinned successfully.")
    def delete(ns, *args, **kwargs):
        """Unpins the IPFS address from the local node. This removes only the local copy of the file from the node, the file will continue to exist in the IPFS network.

        """
        kwargs.update({})
        kwargs["_data"] = request.json
        kwargs["_request"] = request

        mod, call = import_fqn("datacustodian.ipfs.unpin")
        results = call(*args, **kwargs)
        return results, 200
        
    


for nspec in ns_specs:
    api.add_namespace(namespaces[nspec.name])