from .envelope import Envelope
from .gcp_kms import GcpKms


class GcpEnvelope(Envelope):
    def __init__(self, key_path, credentials=None):
        super(GcpEnvelope, self).__init__(GcpKms(key_path, credentials))
