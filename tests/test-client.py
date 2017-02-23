from oslo_config import cfg


class ReadConfig(object):
    def __init__(self, conf_path):
        self.conf_path = conf_path

        self.opt_group = cfg.OptGroup(name='endpoint',
                                 title='Get the endpoints for keystone')

        self.endpoint_opts = [cfg.StrOpt('endpoint', default='None',
            help=('URL or IP address where OpenStack keystone runs.'))
        ]

        CONF = cfg.CONF
        CONF.register_group(self.opt_group)
        CONF.register_opts(self.endpoint_opts, self.opt_group)

        CONF(default_config_files=[self.conf_path])
        self.AUTH_ENDPOINT = CONF.endpoint.endpoint

    def get_endpoint(self):
        return self.AUTH_ENDPOINT


print ReadConfig('app.conf').get_endpoint()
