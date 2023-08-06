import re

import requests

from .isp import ISPApi
from .utils import key_generator


class VMManager(ISPApi):
    def get_user_session_key(self, username) -> str:
        key = key_generator(32)
        request = dict(
            username=username,
            key=key,
        )
        self.send_request('session.newkey', request)
        return self.get_session_key(username, auth_key=key)

    def create_user(self, username, password=None) -> int:
        """
        Создание пользователя
        :param username: Логин
        :param password: Пароль опционально(Генерируется если не передан)
        :return: ID пользователя
        """
        if not password:
            password = key_generator(16)
        request_data = dict(level=16, name=username, passwd=key_generator(16), confirm=password, sok='ok')
        return int(self.send_request('user.edit', request_data)['id']['$'])

    def delete_user(self, user_id):
        """
        Удаление пользователя
        :param user_id: ID пользователя
        """
        self.send_request('user.delete', dict(elid=user_id))

    def disable_user(self, user_id):
        """
        Отключение пользователя
        :param user_id: ID пользователя
        """
        self.send_request('user.disable', dict(elid=user_id))

    def enable_user(self, user_id):
        """
        Включение пользователя
        :param user_id: ID пользователя
        """
        self.send_request('user.enable', dict(elid=user_id))

    def get_users(self) -> list:
        """
        Возвращает список пользователей
        """
        return self.send_request('user', dict())['elem']

    def create_vm(self, name, user_id, preset, hostnode, vmi, recipe, osname, domain, vsize, mem, vcpu, password,
                  clock_offset, cputune=1000, blkiotune=500, inbound=None, outbound=None, sshpubkey=None):
        """

        :param name: Уникальное название для виртуалки
        :param user_id: ID пользователя владельца(По дефолту ID от кого запрос)
        :param preset: Шаблон виртуальной машины (Его ID из списка)
        :param hostnode: Узел кластера (Его ID из списка)
        :param vmi: Код шаблона (пример: ISPsystem__CentOS-7-amd64)
        :param recipe: Рецепт после установки(Для пустого: 'null',
                       для локальнных: '#local__teamspeak.sh' для ips: 'ISPsystem__bitrixcrm.sh')
        :param osname: Просто имя OS(Можно имя из шаблона)
        :param domain: Доменное имя виртуальной машины(Пока хз что сюда писать)
        :param vsize: Размер основного диска в мебибайтах. После создания изменить нельзя
        :param mem: Объем оперативной памяти в мебибайтах
        :param vcpu: Количество виртуальных процессоров доступных виртуальной машине
        :param password: Пароль суперпользователя, так же для доступа по VNC.
                         Для доступа по VNC используются только первые 8 символов пароля
        :param clock_offset: Установка времени. 'localtime' or 'utc'
        :param cputune: Вес cgroups для CPU. Виртуальная машина с весом 1024 получит приоритет в два раза выше
                        на использование CPU по сравнению с виртуальной машиной с весом 512
        :param blkiotune: Вес использования I/O. Вес cgroups на дисковые операции.
                          Позволяет понизить либо повысить приоритет по сравнению с остальными виртуальными машинами
        :param inbound: Ограничение скорости передачи входящего трафика, KiB/sec (None - неограничен)
        :param outbound: Ограничение скорости передачи исходящего трафика, KiB/sec (None - неограничен)
        :param sshpubkey: Публичные SSH ключи. Строка из ключей разделенных \n
        :return: ID созданной ВМ
        """
        request_data = dict(
            sok='ok',
            name=name,
            user=user_id,
            preset=preset,
            hostnode=hostnode,
            installtype='installtemplate',
            vmi=vmi,
            recipe=recipe,
            osname=osname,
            family='ipv4',
            iptype='public',
            domain=domain,
            vsize=vsize,
            mem=mem,
            vcpu=vcpu,
            password=password,
            confirm=password,
            clock_offset=clock_offset,
            cputune=cputune,
            blkiotune=blkiotune,
            inbound=inbound,
            outbound=outbound,
            sshpubkey=sshpubkey,

        )
        response = self.send_request('vm.edit', request_data)
        return int(response['elid']['$'])

    def get_vm_info(self, vm_id):
        """
        Получение основной информации по вм пример ответа в vm_info.json
        :param vm_id: ID виртуалки
        :return:
        """

        return self.send_request('vm.edit', dict(elid=vm_id))

    def get_vnc_url(self, vm_id, username) -> str:
        session_key = self.get_user_session_key(username)
        return f"{self.url}?auth={session_key}&func=novnc&elid={vm_id}"

    def vm_start(self, vm_id):
        self.send_request('vm.start', dict(elid=vm_id))

    def vm_stop(self, vm_id):
        self.send_request('vm.stop', dict(elid=vm_id))

    def vm_restart(self, vm_id):
        self.send_request('vm.restart', dict(elid=vm_id))

    def vm_change_pass(self, vm_id, new_password=None) -> str:
        """
        Смена пароля root
        :param vm_id:
        :param new_password: Пароль который нужно установить
        :return: в ответ возвращает установленный пароль
        """
        if not new_password:
            new_password = key_generator(12)

        self.send_request('vm.chpasswd', dict(elid=vm_id, password=new_password, confirm=new_password, sok='ok'))
        return new_password

    def vm_reinstall(self, vm_id, vmi, recipe, osname, new_password=None, password=None, sshpubkey=None):
        """
        :param vm_id: ID виртуалки
        :param vmi: Код шаблона (пример: ISPsystem__CentOS-7-amd64)
        :param recipe: Рецепт после установки(Для пустого: 'null',
                       для локальнных: '#local__teamspeak.sh' для ips: 'ISPsystem__bitrixcrm.sh')
        :param osname: Просто имя OS(Можно имя из шаблона)
        :param new_password: Установить ли новый пароль? Bool
        :param password: Пароль для установки
        :param sshpubkey: Публичные SSH ключи. Строка из ключей разделенных \n
        :return:
        """
        new_password = 'on' if new_password else None
        request_data = dict(
            sok='ok',
            elid=vm_id,
            vmi=vmi,
            recipe=recipe,
            osname=osname,
            new_password=new_password,
            sshpubkey=sshpubkey,
        )
        if new_password:
            request_data.update(dict(
                password=password,
                confirm=password,
            ))
        return self.send_request('vm.reinstall', request_data)

    def vm_remove(self, vm_id):
        return self.send_request('vm.delete', dict(elid=vm_id, sok='ok'))

    def change_owner(self, vm_id, user_id):
        return self.send_request('vm.edit', dict(elid=vm_id, user=user_id, sok='ok'))

    def get_host(self, host_id):
        return self.send_request('vmhostnode.edit', dict(elid=host_id))

    def get_host_info(self, host_id):
        return self.send_request('vmhostnode.info', dict(elid=host_id))

    def get_host_usedmem(self, host_id):
        host_info = self.get_host_info(host_id)
        for item in host_info['elem']:
            if item['type']['$orig'] == 'paid_mem':
                return int(re.search(r'\d+', item['info']['$']).group())

    def get_hosts(self):
        return self.send_request('vmhostnode', dict())

    def get_ostemplate(self, template_id):
        return self.send_request('osmgr.edit', dict(elid=template_id))

    def suspend_all_rights(self, user_id, username):
        elids = []
        result = self.send_request('userrights', dict(elid=user_id))['elem']
        for item in result:
            elids.append(item['name']['$'])
            children = self.send_request('userrights', dict(plid=username, elid=item['name']['$'])).get('elem', [])
            for child in children:
                elids.append(child['name']['$'])
        elids.remove('vm.novnc')
        elids = ', '.join(elids)
        self.send_request('userrights.suspend', dict(elid=elids, plid=username))
