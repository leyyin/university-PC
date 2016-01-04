# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import Group
from django.db import migrations, models


# def add_group_permissions(first, second):
#     print(first, second)
#     groups = {
#         # group name: list of permissions
#         "student": [],
#         "teacher": [],
#         "admin": []
#     }
#     print("APPLYING MIGRATIONS")
#     for name, permissions in groups:
#         group, created = Group.objects.get_or_create(name=name)
#         if created:
#             # for permission in permissions:
#             #     groups.permissions.add(permission)
#
#             print("{0} group created".format(name))
#     #read_only
#
#     # if created:
#     #     group.permissions.add(can_read_campaign)
#     #     print('read_only_user Group created')
#     #a
#     # #standard
#     # group, created = Group.objects.get_or_create(name='standard_user')
#     # if created:
#     #     group.permissions.add(can_edit_users)
#     #     logger.info('standard_user Group created')
#     #
#     # #admin
#     # group, created = Group.objects.get_or_create(name='admin')
#     # if created:
#     #     group.permissions.add(can_edit_campaign, can_edit_users)
#     #     logger.info('admin_user Group created')


class Migration(migrations.Migration):

    dependencies = [
        ('elearning', '0001_initial'),
    ]

    # see https://docs.djangoproject.com/en/1.8/ref/migration-operations/#runsql
    operations = [
        # migrations.RunSQL(
        #         [("INSERT INTO auth_group(`name`) VALUES({0});", ['admin', 'teacher', 'admin'])],
        #         [("DELETE FROM auth_group WHERE name={0};", ['admin', 'teacher', 'admin'])],
        # )
        # migrations.RunPython(add_group_permissions),
    ]
