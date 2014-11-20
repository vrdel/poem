"""
Profile Management Web API is implemented using
`Django Piston <https://bitbucket.org/jespern/django-piston/wiki/Documentation>`_
and follows its conventions. The implementation has two set of piston handlers, the first one
generates the output for POEM models (via Django ORM):
 * :py:class:`poem_api.handlers.NamespaceHandler`
 * :py:class:`poem_api.handlers.ProfileHandler`
 * :py:class:`poem_api.handlers.MetricInstanceHandler`

This group is accessed by poem-sync to synchronize profiles to a local instance.
The second group implements custom resources to provide support for jQuery widgets (e.g. autocomplete):
 * :py:class:`poem_api.handlers.SuggestionHandler`
 * :py:class:`poem_api.handlers.MetricHandler`
 * :py:class:`poem_api.handlers.TagsHandler`

This group is used to implement AJAX calls for POEM Admin widgets.
Current API is read-only as only GET method calls are supported.

.. note::

    Please note that internal API can change without any prior notice and only
    supports internal SAM components.

"""

from django.http import HttpResponse, HttpResponseNotFound,\
    HttpResponseBadRequest, HttpResponseServerError
from django.conf import settings
from django.core.cache import cache
from django.utils.datastructures import MultiValueDictKeyError
from django.utils import simplejson
from django.core.serializers.json import DateTimeAwareJSONEncoder

from piston import handler
from piston.emitters import Emitter
from piston.handler import typemapper

from Poem.poem import models


class NamespaceHandler(handler.BaseHandler):
    """
    Lists the namespace for which the POEM Web instance was registered. A set of
    namespaces that can be synchronized needs to be unique. Therefore it is a
    good practice to add domain to your namespace. Sample output:
    ::
        { "namespace": "ch.cern.sam" }

    * *Configuration*: POEM_NAMESPACE yaim variable.
    * *URL*: ``/api/0.1/<format>/namespace``
    * *Supported formats*: xml, json
    * *Supported methods*: GET
    """
    methods_allowed = ('GET',)

    def read(self, request):
        return { 'namespace': settings.POEM_NAMESPACE }


class MetricsInProfile(handler.BaseHandler):
    """
    Dumps all metrics, service flavours and profile names
    for a given VO. Example:
    [
        {
            "service_flavour": "APEL",
            "fqan": "",
            "profile__name": "ROC_OPERATORS",
            "metric": "org.apel.APEL-Pub",
            "vo": "ops"
        },
        {
            "service_flavour": "ARC-CE",
            "fqan": "",
            "profile__name": "ROC_OPERATORS",
            "metric": "org.nordugrid.ARC-CE-ARIS",
            "vo": "ops"
        },
    ]
    * *Supported formats*: xml, json
    * *URL*: ``/api/0.1/<format>/metrics_in_profile/?vo_name=ops[&profile_name=ROC]``
    * *Supported methods*: GET
    """

    allowed_methods = ('GET',)
    model = models.MetricInstance
    fields = ('profile_name', 'service_flavour', 'metric', 'vo', 'fqan')

    def read(self, request, attribute):
        lookup = request.GET.get("vo_name")
        if lookup:
            result = models.MetricInstance.objects.filter(vo__exact=lookup)
            result = result.values('profile__name', 'service_flavour', 'vo', 'fqan', 'metric')
            profile = request.GET.get("profile_name")
            if profile:
                result = result.filter(profile__name__exact=profile)
            return result
        else:
            return HttpResponseServerError("Need the name of VO")


class ProfileHandler(handler.BaseHandler):
    """
    Dumps the list of profiles available in this namespace. This API call is used by the
    poem-sync synchronizer to get list of profiles and their attributes. Sample output:
    ::
        [ {
        "name": "ALICE",
        "atp_vo": "alice",
        "metric_instances": [
            {
                "atp_service_type_flavour": "CE",
                "fqan": "",
                "metric": "org.sam.CE-JobSubmit",
                "vo": "alice"
            }, ....
        ] ]

    * *Supported formats*: xml, json
    * *URL*: ``/api/0.1/<format>/profiles``
    * *Supported methods*: GET
    """
    model = models.Profile
    allowed_methods = ('GET')
    fields = ('id', 'name', 'version', 'vo',
              'owner', 'description',
              ('metric_instances', ('metric', 'fqan', 'vo', 'service_flavour')),
             )

class MetricInstanceHandler(handler.BaseHandler):
    """
    Lists all unique metric instances registered in the DB. Metric instance is a tuple
    ``('metric', 'atp_service_type_flavour', 'vo', 'fqan')``. This information is used
    by the poem synchronizer. Sample output:
    ::
        [ {
        "metric": "org.apel.APEL-Pub",
        "fqan": "",
        "atp_service_type_flavour": "APEL",
        "vo": "ops"
          }, ...
        ]

    * *URL*: ``/api/0.1/<format>/metricinstances``
    * *Supported formats*: xml, json
    * *Supported methods*: GET
    """

    allowed_methods=('GET', )
    model = models.Profile
    fields = ('metric', 'service_flavour', 'vo', 'fqan')

    def read(self, request):
        return models.MetricInstance.objects.distinct()


class MetricHandler(handler.BaseHandler):
    """
    Helper resource to lookup metrics based on a term. This is used by the autocomplete
    widgets in Django Admin. For a sample call
    ``/api/0.1/json/hints/metrics/?term=CE`` the following output is provided:
    ::
        [
        "org.sam.CREAMCE-JobState",
        "org.sam.CREAMCE-DirectJobState",
        "org.sam.mpi.CE-JobSubmit", ...
        ]

    * *URL*: ``/api/0.1/json/hints/metrics/``
    * *Supported formats*: json
    * *Supported methods*: GET
    """

    allowed_methods=('GET',)
    fields= ('metric')
    model = models.MetricInstance

    def read(self, request):
        if 'term' in request.GET:
            term = request.GET.get('term')
            qs = models.MetricInstance.objects.filter(metric__contains=term).\
                values_list('metric').distinct()
            return set(map(lambda x: x[0], qs))
        else:
            qs = models.MetricInstance.objects.all().values_list('metric').\
                distinct()
            return set(map(lambda x: x[0], qs))

class SuggestionHandler(handler.BaseHandler):
    """
    Helper resource to lookup ATP attributes (e.g. VO, flavours) by calling ATP API. This is used by the autocomplete
    widgets in Django Admin. For a sample call
    ``/api/0.1/json/hints/atp_vo/?term=alice`` the following output is provided:
    ::
        [ "calice", "alice" ]

    * *Configuration*: ATP API mapping for given attribute is configured in settings via
                               SUGGESTION_URIS and SUGGESTION_KEYS
    * *URL*: ``/api/1.1/json/hints/<atp_attribute>/?term=<lookup_term>``
    * *Supported formats*: json
    * *Supported methods*: GET
    """

    allowed_methods=('GET',)
    fields = ('name',)

    def read(self, request, attribute):
        cache_key = request.path.split('?')[0]
        lookup = request.GET.get('term')

        if not cache.get(cache_key):
            if attribute == "vo":
                values = [vo.name for vo in models.VO.objects.all()]
            elif attribute == "service_flavours":
                values = [sf.name for sf in models.ServiceFlavour.objects.all()]
            cache.set(cache_key, values)
        else:
            values = cache.get(cache_key)

        return sorted(filter(lambda x: lookup.lower() in x.lower(), values))
