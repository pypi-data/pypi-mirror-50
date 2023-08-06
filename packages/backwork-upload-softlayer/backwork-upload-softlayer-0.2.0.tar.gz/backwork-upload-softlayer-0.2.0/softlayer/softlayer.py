"""Upload file to Softlayer storage options."""
import logging
import object_storage

LOG = logging.getLogger(__name__)


class ObjectStorageUpload(object):  # pylint: disable=unused-variable
    """Upload a file to Softlayer ObjectStorage."""
    command = "softlayer"

    def __init__(self, args, extra):
        self.args = args
        self.extra = extra
        self.client = object_storage.get_client(
            self.args.username,
            self.args.api_key,
            datacenter=self.args.datacenter,
            network=self.args.network)

    @classmethod
    def parse_args(cls, subparsers):
        """Add Softlayer ObjectStorage arguments to command line parser."""
        sl_oo_parser = subparsers.add_parser("softlayer", description=cls.__doc__)

        sl_oo_parser.add_argument("-u", "--username",
                                  help="username for Softlayer ObjectStorage API")
        sl_oo_parser.add_argument("-p", "--api-key",
                                  help="api key for Softlayer ObjectStorage API")
        sl_oo_parser.add_argument("-d", "--datacenter",
                                  help="datacenter where the file will be stored")
        sl_oo_parser.add_argument("-c", "--container",
                                  help="target container")
        sl_oo_parser.add_argument("-n", "--network", default="private",
                                  help="'public' or 'private' Softlayer network")

        sl_oo_parser.add_argument("local_path", nargs="?", default=None,
                                  help="path in the local file system of the file to be uploaded")
        sl_oo_parser.add_argument("remote_path",
                                  help="""path on Softlayer ObjectStorage container where the file
                                  will be stored""")

    def upload(self):
        """Upload a file from `local_path` to `remote_path` on ObjectStorage."""
        LOG.info("uploading '%s' to Softlayer ObjectStorage", self.args.local_path)
        LOG.info("target path: '%s/%s' at '%s'", self.args.container, self.args.remote_path,
                 self.args.datacenter)

        container = self.client[self.args.container]

        # make sure target container exists
        if container.name not in [c.name for c in self.client.containers()]:
            LOG.info("container '%s' not found. creating it...", self.args.container)
            container.create()

        with open(self.args.local_path) as needle:
            container[self.args.remote_path].create()
            container[self.args.remote_path].send(needle)

        LOG.info("upload complete")
