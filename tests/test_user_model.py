# -*- coding: utf-8 -*-
__author__ = 'lihui'

import unittest
from app.models import User, Role, Permission, AnonymousUser


class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User(password = 'dog')
        self.assertTrue(u.password_hash is not None)

    def test_password_getter(self):
        u = User(password='dog')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password = 'dog')
        self.assertFalse(u.verify_password('cat'))
        self.assertTrue(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = User(password = 'dog')
        u2 = User(password = 'dog')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_roles_and_permissions(self):
        Role.insert_roles()
        u = User(email='lihui@fanxiangce.com', password="secret")
        self.assertTrue(u.can(Permission.CREATE_ALBUMS))
        self.assertFalse(u.can(Permission.MODRATE_COMMENTS))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.CREATE_ALBUMS))