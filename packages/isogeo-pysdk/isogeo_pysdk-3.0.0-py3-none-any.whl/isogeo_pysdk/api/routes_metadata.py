# -*- coding: UTF-8 -*-
#! python3

"""
    Isogeo API v1 - API Routes for Resources (= Metadata) entity

    See: http://help.isogeo.com/api/complete/index.html#definition-resource
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from urllib.parse import urlparse, parse_qs, urlunparse

# 3rd party
import requests
from requests.adapters import HTTPAdapter
from requests.models import Response

# submodules
from isogeo_pysdk.exceptions import AlreadyExistError
from isogeo_pysdk.checker import IsogeoChecker
from isogeo_pysdk.decorators import ApiDecorators
from isogeo_pysdk.models import Metadata, ResourceSearch
from isogeo_pysdk.utils import IsogeoUtils

# other routes
from .routes_event import ApiEvent
from .routes_feature_attributes import ApiFeatureAttribute
from .routes_service_layers import ApiServiceLayer
from .routes_service_operations import ApiServiceOperation

# #############################################################################
# ########## Globals ###############
# ##################################

logger = logging.getLogger(__name__)
checker = IsogeoChecker()
utils = IsogeoUtils()


# #############################################################################
# ########## Classes ###############
# ##################################
class ApiMetadata:
    """Routes as methods of Isogeo API used to manipulate metadatas (resources).
    """

    def __init__(self, api_client=None):
        if api_client is not None:
            self.api_client = api_client

        # store API client (Request [Oauthlib] Session) and pass it to the decorators
        self.api_client = api_client
        ApiDecorators.api_client = api_client

        # ensure platform to request
        self.platform, self.api_url, self.app_url, self.csw_url, self.mng_url, self.oc_url, self.ssl = utils.set_base_url(
            self.api_client.platform
        )

        # sub routes
        self.attributes = ApiFeatureAttribute(self.api_client)
        self.events = ApiEvent(self.api_client)
        self.layers = ApiServiceLayer(self.api_client)
        self.operations = ApiServiceOperation(self.api_client)

        # initialize
        super(ApiMetadata, self).__init__()

    @ApiDecorators._check_bearer_validity
    def get(self, metadata_id: str, include: list or str = []) -> Metadata:
        """Get complete or partial metadata about a specific metadata (= resource).

        :param str metadata_id: metadata UUID to get
        :param list include: subresources that should be included. Available values:

          - one or various from MetadataSubresources (Enum)
          - "all" to get complete metadata with every subresource included
        """
        # check metadata UUID
        if not checker.check_is_uuid(metadata_id):
            raise ValueError(
                "Metadata ID is not a correct UUID: {}".format(metadata_id)
            )
        else:
            pass

        # request parameters
        payload = {
            "_include": checker._check_filter_includes(
                includes=include, entity="metadata"
            )
        }

        # URL
        url_resource = utils.get_request_base_url(
            route="resources/{}".format(metadata_id)
        )

        # request
        req_resource = self.api_client.get(
            url=url_resource,
            headers=self.api_client.header,
            params=payload,
            proxies=self.api_client.proxies,
            timeout=self.api_client.timeout,
            verify=self.api_client.ssl,
        )

        # checking response
        req_check = checker.check_api_response(req_resource)
        if isinstance(req_check, tuple):
            return req_check

        # handle bad JSON attribute
        metadata = req_resource.json()
        metadata["coordinateSystem"] = metadata.pop("coordinate-system", list)
        metadata["featureAttributes"] = metadata.pop("feature-attributes", list)

        # end of method
        return Metadata(**metadata)

    @ApiDecorators._check_bearer_validity
    def create(
        self, workgroup_id: str, metadata: Metadata, check_exists: int = 1
    ) -> Metadata:
        """Add a new metadata to a workgroup.

        :param str workgroup_id: identifier of the owner workgroup
        :param Metadata metadata: Metadata model object to create
        :param int check_exists: check if a metadata with the same title already exists into the workgroup:

        - 0 = no check
        - 1 = compare name [DEFAULT]
        """
        # check workgroup UUID
        if not checker.check_is_uuid(workgroup_id):
            raise ValueError("Workgroup ID is not a correct UUID.")
        else:
            pass

        # check if metadata already exists in workgroup
        # if check_exists == 1:
        #     # retrieve workgroup metadatas
        #     if not self.api_client._wg_metadatas_names:
        #         self.metadatas(workgroup_id=workgroup_id, include=[])
        #     # check
        #     if metadata.name in self.api_client._wg_metadatas_names:
        #         logger.debug(
        #             "Metadata with the same name already exists: {}. Use 'metadata_update' instead.".format(
        #                 metadata.name
        #             )
        #         )
        #         return False
        # else:
        #     pass

        # build request url
        url_metadata_create = utils.get_request_base_url(
            route="groups/{}/resources".format(workgroup_id)
        )

        # request
        req_new_metadata = self.api_client.post(
            url=url_metadata_create,
            json=metadata.to_dict_creation(),
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_new_metadata)
        if isinstance(req_check, tuple):
            return req_check

        # load new metadata and save it to the cache
        new_metadata = Metadata(**req_new_metadata.json())
        # self.api_client._wg_metadatas_names[new_metadata.name] = new_metadata._id

        # end of method
        return new_metadata

    @ApiDecorators._check_bearer_validity
    def delete(self, metadata_id: str) -> Response:
        """Delete a metadata from Isogeo database.

        :param str metadata_id: identifier of the resource to delete
        """
        # check metadata UUID
        if not checker.check_is_uuid(metadata_id):
            raise ValueError(
                "Metadata ID is not a correct UUID: {}".format(metadata_id)
            )
        else:
            pass

        # request URL
        url_metadata_delete = utils.get_request_base_url(
            route="resources/{}".format(metadata_id)
        )

        # request
        req_metadata_deletion = self.api_client.delete(
            url_metadata_delete,
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_metadata_deletion)
        if isinstance(req_check, tuple):
            return req_check

        return req_metadata_deletion

    @ApiDecorators._check_bearer_validity
    def exists(self, resource_id: str) -> bool:
        """Check if the specified resource exists and is available for the authenticated user.

        :param str resource_id: identifier of the resource to verify
        """
        # check metadata UUID
        if not checker.check_is_uuid(resource_id):
            raise ValueError(
                "Resource ID is not a correct UUID: {}".format(resource_id)
            )
        else:
            pass

        # URL builder
        url_metadata_exists = "{}{}".format(
            utils.get_request_base_url("resources"), resource_id
        )

        # request
        req_metadata_exists = self.api_client.get(
            url=url_metadata_exists,
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_metadata_exists)
        if isinstance(req_check, tuple):
            return req_check

        return True

    @ApiDecorators._check_bearer_validity
    def update(self, metadata: Metadata) -> Metadata:
        """Check if the specified resource exists and is available for the authenticated user.

        :param Metadata metadata: metadata object to update
        """
        # check metadata UUID
        if not checker.check_is_uuid(metadata._id):
            raise ValueError(
                "Resource ID is not a correct UUID: {}".format(metadata._id)
            )
        else:
            pass

        # URL builder
        url_metadata_exists = utils.get_request_base_url(
            route="resources/{}".format(metadata._id)
        )

        # request
        req_metadata_exists = self.api_client.patch(
            url=url_metadata_exists,
            json=metadata.to_dict_creation(),
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_metadata_exists)
        if isinstance(req_check, tuple):
            return req_check

        return True

    # -- Routes to search --------------------------------------------------------------
    @ApiDecorators._check_bearer_validity
    def search(
        self,
        # semantic and objects filters
        query: str = "",
        share: str = None,
        specific_md: list = [],
        # results model
        include: list = [],
        # geographic filters
        bbox: list = None,
        poly: str = None,
        georel: str = None,
        # sorting
        order_by: str = "_created",
        order_dir: str = "desc",
        # results size
        page_size: int = 20,
        offset: int = 0,
        # specific options of implemention
        # augment: bool = False,
        check: bool = True,
        # tags_as_dicts: bool = False,
        # whole_share: bool = True,
    ) -> ResourceSearch:
        """Search within the resources shared to the application. It's the mainly used method to retrieve metadata.

        :param str query: search terms and semantic filters. Equivalent of
         **q** parameter in Isogeo API. It could be a simple
         string like *oil* or a tag like *keyword:isogeo:formations*
         or *keyword:inspire-theme:landcover*. The *AND* operator
         is applied when various tags are passed.
        :param list bbox: Bounding box to limit the search. Must be a 4 list of coordinates in WGS84 (EPSG 4326). Could be associated with *georel*.
        :param str poly: Geographic criteria for the search, in WKT format. Could be associated with *georel*.
        :param str georel: geometric operator to apply to the `bbox` or `poly` parameters. Available values:

            * 'contains',
            * 'disjoint',
            * 'equals',
            * 'intersects' - [APPLIED BY API if NOT SPECIFIED]
            * 'overlaps',
            * 'within'.

        :param str order_by: sorting results. Available values:

            * '_created': metadata creation date [DEFAULT if relevance is null]
            * '_modified': metadata last update
            * 'title': metadata title
            * 'created': data creation date (possibly None)
            * 'modified': data last update date
            * 'relevance': relevance score calculated by API [DEFAULT].

        :param str order_dir: sorting direction. Available values:

            * 'desc': descending
            * 'asc': ascending

        :param int page_size: limits the number of results.
         Useful to paginate results display. Default value: 100.
        :param int offset: offset to start page size
         from a specific results index
        :param str share: share UUID to filter on
        :param list specific_md: list of metadata UUIDs to filter on
        :param list include: subresources that should be returned.
         Must be a list of strings. Available values: *isogeo.SUBRESOURCES*
        :param bool whole_share: option to return all results or only the
         page size. *True* by DEFAULT.
        :param bool check: option to check query parameters and avoid erros.
         *True* by DEFAULT.
        :param bool augment: option to improve API response by adding
         some tags on the fly (like shares_id)
        :param bool tags_as_dicts: option to store tags as key/values by filter.
        """
        # handling request parameters
        payload = {
            "_id": checker._check_filter_specific_md(specific_md),
            "_include": checker._check_filter_includes(
                includes=include, entity="metadata"
            ),
            "_limit": page_size,
            "_offset": offset,
            "box": bbox,
            "geo": poly,
            "rel": georel,
            "ob": order_by,
            "od": order_dir,
            "q": query,
            "s": share,
        }

        # check params
        if check:
            checker.check_request_parameters(payload)
        else:
            pass

        # URL
        url_resources_search = utils.get_request_base_url(route="resources/search")

        # request
        req_metadata_search = self.api_client.get(
            url=url_resources_search,
            headers=self.api_client.header,
            params=payload,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=(5, 200),
        )

        # checking response
        req_check = checker.check_api_response(req_metadata_search)
        if isinstance(req_check, tuple):
            return req_check

        # end of method
        return ResourceSearch(**req_metadata_search.json())

    # def workgroup_metadata(
    #     self,
    #     workgroup_id: str,
    #     order_by: str = "_created",
    #     order_dir: str = "desc",
    #     page_size: int = 100,
    #     offset: int = 0,
    # ) -> dict:
    #     """List workgroup metadata.

    #     :param str workgroup_id: identifier of the owner workgroup
    #     """
    #     # check workgroup UUID
    #     if not checker.check_is_uuid(workgroup_id):
    #         raise ValueError("Workgroup ID is not a correct UUID.")
    #     else:
    #         pass

    #     # request parameters
    #     payload = {
    #         # "_include": include,
    #         # "_lang": self.lang,
    #         "_limit": page_size,
    #         "_offset": offset,
    #         "ob": order_by,
    #         "od": order_dir,
    #         # "q": query,
    #         # "s": share,
    #     }

    #     # build request url
    #     url_metadata_list = utils.get_request_base_url(
    #         route="groups/{}/resources/search".format(workgroup_id)
    #     )

    #     wg_metadata = self.api_client.get(
    #         url_metadata_list,
    #         headers=self.api_client.header,
    #         params=payload,
    #         proxies=self.api_client.proxies,
    #         verify=self.api_client.ssl,
    #         timeout=self.api_client.timeout,
    #     )

    #     wg_metadata = wg_metadata.json()

    #     # # if caching use or store the workgroup metadata
    #     # if caching and not self._wg_apps_names:
    #     #     self._wg_apps_names = {i.get("name"): i.get("_id") for i in wg_metadata}

    #     return wg_metadata

    # -- Helpers for services ---------------------------------------------------------


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """ standalone execution """
    api_metadata = ApiMetadata()
    print(api_metadata)
