from security_monkey.cloudaux_watcher import CloudAuxWatcher
from cloudaux.aws.elb import describe_load_balancers
from cloudaux.orchestration.aws.elb import get_load_balancer
from security_monkey import app


class ELB(CloudAuxWatcher):
    index = 'elb'
    i_am_singular = 'ELB'
    i_am_plural = 'ELBs'
    honor_ephemerals = False
    ephemeral_paths = list()
    service_name = 'elb'
    detail = app.config.get('SECURITYGROUP_INSTANCE_DETAIL', 'FULL')

    def get_name_from_list_output(self, item):
        return item['LoadBalancerName']

    def list_method(self, **kwargs):
        return describe_load_balancers(**kwargs)

    def get_method(self, item, **kwargs):
        result = get_load_balancer(item, **kwargs)
        if self.detail == 'NONE' or self.detail == None:
            result.pop('Instances', None)
        elif self.detail == 'SUMMARY':
            result['Instances'] = '{len} Instance(s)'.format(len=len(result.get('Instances', [])))
        return result
