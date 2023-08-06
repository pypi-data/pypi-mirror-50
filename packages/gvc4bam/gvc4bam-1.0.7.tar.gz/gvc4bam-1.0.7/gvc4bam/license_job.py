from toil.common import Toil
from toil.job import Job

from runner.runner import docker_runner, decorator_wrapt


class verify_license(Job):
    @decorator_wrapt
    def __init__(self, image, volumes, *args, **kwargs):
        self.image = image
        self.volumes = volumes
        self.commandLine = ['check_license']
        return super(verify_license, self).__init__(*args, **kwargs)

    @docker_runner("verify_license")
    def run(self,fileStore):
        return self.commandLine


    



