from dataclasses import asdict, dataclass
from typing import Dict, Optional

from zabier.zabbix.base import ZabbixBase


@dataclass
class Template:
    templateid: Optional[str]
    host: str
    name: str
    description: str


class TemplateMixin(ZabbixBase):
    def create_host_group(self, template: Template) -> int:
        response: Dict = self.do_request(
            "template.create",
            asdict(template)
        )
        return response['result']['templateids'].pop()

    def get_template_by_name(self, name:str) -> Optional[Template]:
        response: Dict = self.do_request(
            "template.get",
            {
                "search": {
                    "name": [name]
                },
                "editable": True,
                "startSearch": True,
                "searchByAny": True
            }
        )
        if len(response['result']) == 0:
            return None
        template = response['result'].pop()
        return Template(
            templateid=template['templateid'],
            host=template['host'],
            name=template['name'],
            description=template['description'])
