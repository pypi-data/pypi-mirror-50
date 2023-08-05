import os

class Qvf():

    def __init__(self, qvf='', path=os.getcwd()):
        self.qvf_path = path
        self.qvf_name = qvf
        self.qvf_size_mb = os.path.getsize(self.qvf_path + self.qvf_name) / 1000000

    