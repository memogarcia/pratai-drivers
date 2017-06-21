import os
import uuid

from StringIO import StringIO


def build_dockerfile(zip_location, runtime='python27', template_path='templates/'):
    """Build a Dockerfile from template

    :param zip_location: an accessible url where the driver can retrieve the
    user code
    :param template_path: a Dockerfile template
    :return: a Dockerfile that will be used by the driver
    """

    zip_file = zip_location[-36:]
    if runtime == 'python27':
        template = '{0}{1}.txt'.format(template_path, runtime)
    else:
        return
    dockerfile = StringIO()
    with open(template, 'r') as temp:
        for line in temp.readlines():
            if '{zip_location}' in line:
                l = line.replace('{zip_location}', zip_location)
                dockerfile.write(l)
                continue
            if '{zip_file}' in line:
                l = line.replace('{zip_file}', zip_file)
                dockerfile.write(l)
                continue
            dockerfile.write(line)

    return dockerfile.getvalue()


def save_dockerfile(zip_location, runtime='python27', path='/tmp/'):
    """Save Dockerfile to filesystem

    :param zip_location: an accessible url where the driver can retrieve the
    user code
    :param path:  path to store the Dockefile
    :return: Dockerfile path
    """
    uuid1 = uuid.uuid4().hex
    new_path = "{0}{1}/".format(path, uuid1)
    os.mkdir(new_path)
    dockerfile = "{0}Dockerfile".format(new_path)
    with open(dockerfile, 'wb') as df:
        df.write(build_dockerfile(zip_location, runtime=runtime))

    return new_path


def build_tags(tags):
    tag_string = ""
    if tags:
        for tag in tags:
            tag_string += " -t {0}".format(tag)


def build_args(req):
    # TODO(m3m0): check memory and swap
    memory = req.get("memory")
    tags = req.get("tags", [])
    zip_location = req.get("zip_location")

    runtime = req.get("runtime")
    dockerfile = save_dockerfile(zip_location, runtime=runtime)

    tag_string = ""
    if tags:
        for tag in tags:
            tag_string += " -t {0}".format(tag)

    # TODO(m3m0): --no-cache as a parameter

    cmd = "build --force-rm=true {0} {1}".format(tag_string, dockerfile)
    return cmd
