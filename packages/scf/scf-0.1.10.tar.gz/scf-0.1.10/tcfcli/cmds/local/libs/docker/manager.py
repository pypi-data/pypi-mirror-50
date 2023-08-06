# -*- coding: utf-8 -*-

import docker
import click


class ContainerManager(object):
    def __init__(self,
                 docker_network_id=None,
                 skip_pull_image=False,
                 is_quiet=False):

        self._docker_network_id = docker_network_id
        self._skip_pull_image = skip_pull_image
        self._docker_client = docker.from_env()

        self._is_quiet = is_quiet

    def run(self, container):
        image = container.image

        if not self.has_image(image) or not self._skip_pull_image:
            self.pull_image(image)
        else:
            if not self._is_quiet:
                click.secho('skip pull image %s' % image)

        if not container.is_exist():
            container.create()

        container.start()

    def stop(self, container):
        pass

    def pull_image(self, image):
        try:
            if not self._is_quiet:
                click.secho('pull image %s...' % image, nl=False)
            for _ in self._docker_client.api.pull(image, stream=True, decode=True):
                if not self._is_quiet:
                    click.secho('.', nl=False)
            if not self._is_quiet:
                click.secho('\n')
        except docker.errors.APIError as e:
            raise Exception('pull the docker image %s failed, %s' % (image, str(e)))

    def has_image(self, image):
        try:
            self._docker_client.images.get(image)
            return True
        except docker.errors.ImageNotFound:
            return False
