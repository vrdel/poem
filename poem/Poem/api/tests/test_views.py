import json

from mock import patch

from rest_framework.test import APITestCase, APIRequestFactory, \
    force_authenticate
from rest_framework import status

from rest_framework_api_key.models import APIKey
from rest_framework_api_key.crypto import _generate_token, hash_token

from Poem.poem.models import *
from Poem.api.views import *

from reversion.models import Version


def mock_db_for_tagged_metrics_tests():
    tag1 = Tags.objects.create(name='prod')
    tag2 = Tags.objects.create(name='test_none')
    Tags.objects.create(name='test_empty')

    metrictype = MetricType.objects.create(name='active')

    probekey = Version.objects.create(
        object_repr='ams_probe (0.1.7)',
        serialized_data=json.dumps(
            [
                {
                    'model': 'poem.probe',
                    'fields': {
                        'comment': 'Initial version',
                        'group': 'EOSC',
                        'version': '0.1.7',
                        'docurl':
                            'https://github.com/ARGOeu/nagios-plugins-argo'
                            '/blob/master/README.md'
                    }
                }
            ]
        ),
        content_type_id='1',
        revision_id='1'
    )

    metric1 = Metric.objects.create(
        name='argo.AMS-Check',
        tag=tag1,
        mtype=metrictype,
        probekey=probekey,
    )

    group = GroupOfMetrics.objects.create(name='EOSC')
    group.metrics.create(name=metric1.name)

    MetricParent.objects.create(
        metric=metric1,
        value='org.nagios.CDMI-TCP'
    )

    MetricProbeExecutable.objects.create(
        metric=metric1,
        value='ams-probe'
    )

    MetricConfig.objects.create(
        key='maxCheckAttempts',
        value='3',
        metric=metric1
    )
    MetricConfig.objects.create(
        key='timeout',
        value='60',
        metric=metric1
    )
    MetricConfig.objects.create(
        key='path',
        value='/usr/libexec/argo-monitoring/probes/argo',
        metric=metric1
    )
    MetricConfig.objects.create(
        key='interval',
        value='5',
        metric=metric1
    )
    MetricConfig.objects.create(
        key='retryInterval',
        value='3',
        metric=metric1
    )

    MetricAttribute.objects.create(
        key='argo.ams_TOKEN',
        value='--token',
        metric=metric1
    )

    MetricDependancy.objects.create(
        key='argo.AMS-Check',
        value='1',
        metric=metric1
    )

    MetricFlags.objects.create(
        key='OBSESS',
        value='1',
        metric=metric1
    )

    MetricFiles.objects.create(
        key='UCC_CONFIG',
        value='UCC_CONFIG',
        metric=metric1
    )

    MetricParameter.objects.create(
        key='--project',
        value='EGI',
        metric=metric1
    )

    MetricFileParameter.objects.create(
        key='FILE_SIZE_KBS',
        value='1000',
        metric=metric1
    )

@patch('Poem.api.permissions.SECRET_KEY', 'top_secret')
@patch('Poem.api.permissions.TOKEN_HEADER', 'HTTP_X_API_KEY')
class ListTaggedMetricsAPIViewTests(APITestCase):
    def setUp(self):
        token = _generate_token()
        hashed_token = hash_token(token, 'top_secret')
        obj = APIKey.objects.create(client_id='EGI')
        obj.token = token
        obj.hashed_token = hashed_token
        obj.save()
        self.token = token
        self.view = ListTaggedMetrics.as_view()
        self.factory = APIRequestFactory()
        self.url_base = '/api/v2/metrics/'

        mock_db_for_tagged_metrics_tests()

    def test_get_metric_for_a_given_tag_with_all_fields(self):
        request = self.factory.get(self.url_base + 'prod', **{'HTTP_X_API_KEY':
                                                            self.token})
        response = self.view(request, 'prod')
        self.assertEqual(
            response.data,
            [
                {
                    'argo.AMS-Check': {
                        'probe': 'ams-probe',
                        'config': {
                            'maxCheckAttempts': '3',
                            'timeout': '60',
                            'path': '/usr/libexec/argo-monitoring/probes/argo',
                            'interval': '5',
                            'retryInterval': '3'
                        },
                        'flags': {
                            'OBSESS': '1'
                        },
                        'dependency': {
                            'argo.AMS-Check': '1'
                        },
                        'attribute': {
                            'argo.ams_TOKEN': '--token'
                        },
                        'parameter': {
                            '--project': 'EGI'
                        },
                        'file_parameter': {
                            'FILE_SIZE_KBS': '1000'
                        },
                        'file_attribute': {
                            'UCC_CONFIG': 'UCC_CONFIG'
                        },
                        'parent': 'org.nagios.CDMI-TCP',
                        'docurl':
                            'https://github.com/ARGOeu/nagios-plugins-argo'
                            '/blob/master/README.md'
                    }
                }
            ]
        )

    def test_get_metric_with_invalid_tag(self):
        request = self.factory.get(self.url_base + 'invalidtag',
                                   **{'HTTP_X_API_KEY': self.token})
        response = self.view(request, 'invalidtag')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'detail': 'Tag not found'})
