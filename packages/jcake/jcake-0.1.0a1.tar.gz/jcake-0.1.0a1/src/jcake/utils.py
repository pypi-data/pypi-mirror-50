# -*- encoding: utf-8 -*-

import os

from bs4 import BeautifulSoup


__all__ = ['is_maven_project', 'parse_pom']


def is_maven_project():
    """ 检测当前项目是否是基于maven的项目 """
    return os.path.exists('./pom.xml')


class ProjectInfo(object):
    def __init__(self, name, group_id, artifact_id, version):
        self.name = name
        self.group_id = group_id
        self.artifact_id = artifact_id
        self.version = version

    def __repr__(self):
        return 'ProjectInfo({}, {}, {}, {})'.format(
            self.name,
            self.group_id,
            self.artifact_id,
            self.version
        )


def add_module_to_pom(pom_file, module_name):
    """
    向pom文件中增加子模块信息

    """
    content = None
    with open(pom_file, 'r', encoding='utf-8') as pom:
        content = pom.read()
        soup = BeautifulSoup(content, 'xml')

        if soup.project.modules is None:
            return """
<modules>
  <module>{}</module>
</modules>""".format(module_name)
        else:
            return "<module>{}</module>".format(module_name)

    with open(pom_file, 'w', encoding='utf-8') as pom:
        content = content.replace(
            "<packaging>jar</packaging>",
            "<packaging>pom</packaging>"
        )
        pom.write(content)


def parse_pom(pom_file):
    """
    解析pom文件，解析结果携带：项目名称，groupId, artifactId和version信息

    """
    with open(pom_file, 'r', encoding='utf-8') as pom:
        soup = BeautifulSoup(pom.read(), 'xml')

        group_id_node = soup.select_one('project > groupId')
        artifact_id_node = soup.select_one('project > artifactId')
        version_node = soup.select_one('project > version')

        module_name = group_id_node.text.split('.')[-1]
        return ProjectInfo(
            module_name,
            group_id_node.text,
            artifact_id_node.text,
            version_node.text
        )
