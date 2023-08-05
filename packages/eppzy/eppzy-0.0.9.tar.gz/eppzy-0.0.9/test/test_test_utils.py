from eppzy.rfc5733_contact import Contact
from eppzy.rfc5731_domain import Domain
from eppzy.rfc5732_host import Host
from eppzy.test_utils import overlayed
from eppzy.session import RequestWrapper

from util import mocked_session, data_file_contents


def test_domain_overlay():
    rw_check_count = 0

    def rw_checks(body):
        nonlocal rw_check_count
        rw_check_count += 1
        if rw_check_count == 1:
            assert b'info' in body
            return data_file_contents('rfc5730/obj_does_not_exist.xml')
        elif rw_check_count == 2:
            assert b'info' in body
            assert b'contact' in body
            return data_file_contents('rfc5733/contact_info_example.xml')
        elif rw_check_count == 3:
            assert b'create' in body
            assert b'domain' in body
            return data_file_contents('rfc5731/create_example.xml')
        elif rw_check_count == 4:
            assert b'info' in body
            return data_file_contents('rfc5731/domain_info_full_example.xml')
        elif rw_check_count == 5:
            assert b'update' in body
            return data_file_contents('rfc5731/update_example.xml')
        else:
            raise AssertionError('More requests made to rw than expected')

    def ro_checks(body):
        assert b'info' in body
        assert b'domain' in body
        return data_file_contents('rfc5731/domain_info_full_example.xml')
    with mocked_session(rw_checks, [Domain, Contact]) as rws:
        with mocked_session(ro_checks, [Domain, Contact]) as ros:
            o = overlayed(rws, ros)
            r = o['domain'].info('example.com')
            assert r.data['registrant'] == 'jd1234'
            assert rw_check_count == 4
            o['domain'].update(r.data['name'], registrant='Mac')


def _overlay_basic_checks(cls, info_path, create_path, info_args):
    rw_check_count = 0

    def rw_checks(body):
        nonlocal rw_check_count
        rw_check_count += 1
        if rw_check_count == 1:
            assert b'info' in body
            return data_file_contents('rfc5730/obj_does_not_exist.xml')
        elif rw_check_count == 2:
            assert b'create' in body
            return data_file_contents(create_path)
        if rw_check_count == 3:
            assert b'info' in body
            return data_file_contents(info_path)
        raise AssertionError('More rw requests than expected')

    def ro_checks(body):
        assert b'info' in body
        return data_file_contents(info_path)

    with mocked_session(rw_checks, [cls]) as rws:
        with mocked_session(ro_checks, [cls]) as ros:
            overlayed(rws, ros)[cls.name].info(*info_args)
    assert rw_check_count == 3


def test_contact_overlay():
    _overlay_basic_checks(
        Contact, 'rfc5733/contact_info_example.xml',
        'rfc5733/contact_create_example.xml', ('philster', 'pass'))


def test_host_overlay():
    _overlay_basic_checks(
        Host, 'rfc5732/info.xml', 'rfc5732/create.xml', ('ns1.example.com',))
