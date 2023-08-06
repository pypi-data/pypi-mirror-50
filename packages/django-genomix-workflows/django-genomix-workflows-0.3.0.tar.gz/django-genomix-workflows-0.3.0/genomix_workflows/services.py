# -*- coding: utf-8 -*-
import logging

import pandas
from rest_framework.exceptions import ParseError

from .models import Task, Workflow

logger = logging.getLogger(__name__)


def get_or_error(classmodel, **kwargs):
    if 'label' in kwargs and not kwargs.get('label'):
        return None
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist as error:
        raise classmodel.DoesNotExist('Error: {0}. kwargs: {1}'.format(error, kwargs))


def load_tasks(filename, mode="Create", *args, **kwargs):
    """
    Loads Tasks into nexus
    Arguments:
        filename (str): filename of details filename
    Notes:
        file expects the following columns:
            - Task: string
            - Version: string
            - Previous: comma separated list
    """
    df = pandas.read_csv(filename, sep='\t', na_values=['NA', 'na', 'NULL', 'null', 'NONE', 'none', ''])
    df = df.where((pandas.notnull(df)), None)
    columns = df.columns

    for index, row in df.iterrows():
        label = row[columns.get_loc('Task')]
        previous_tasks = row[columns.get_loc('Previous')]
        previous_tasks = previous_tasks.split(',') if previous_tasks else []
        previous_tasks_list = []
        for previous_task in previous_tasks:
            previous_tasks_list.append(get_or_error(Task, label=previous_task))

        if mode.lower() == 'update':
            try:
                instance, _ = Task.objects.get_or_create(
                    label=label,
                    version=float(row[columns.get_loc('Version')])
                )
            except Exception:
                error = 'Could not retrieve Task: {0} v{1}'.format(
                    row[columns.get_loc('Task')],
                    row[columns.get_loc('Version')],
                )
                raise ParseError(detail=error, code='bad_request')
        elif mode.lower() == 'create':
            try:
                instance = Task.objects.create(
                    label=label,
                    version=float(row[columns.get_loc('Version')])
                )
            except Exception:
                error = 'Could not create Task: {0} v{1}'.format(
                    row[columns.get_loc('Task')],
                    row[columns.get_loc('Version')],
                )
                raise ParseError(detail=error, code='bad_request')
        else:
            raise ParseError(detail='Mode: {0} not supported'.format(mode), code='bad_request')

        instance.previous.clear()
        instance.previous.add(*previous_tasks_list)
        instance.save()


def load_workflows(filename, mode="Create", *args, **kwargs):
    """
    Loads Tasks into nexus
    Arguments:
        filename (str): filename of details filename
    Notes:
        file expects the following columns:
            - Workflow: string
            - Version: string
            - Tasks: comma separated list
    """
    df = pandas.read_csv(filename, sep='\t', na_values=['NA', 'na', 'NULL', 'null', 'NONE', 'none', ''])
    df = df.where((pandas.notnull(df)), None)
    columns = df.columns

    for index, row in df.iterrows():
        label = row[columns.get_loc('Workflow')]
        tasks = row[columns.get_loc('Tasks')].split(',')
        task_list = []
        for task in tasks:
            task_list.append(get_or_error(Task, label=task))

        if mode.lower() == 'update':
            try:
                instance, _ = Workflow.objects.get_or_create(
                    label=label,
                    version=float(row[columns.get_loc('Version')]),
                )
            except Exception:
                error = 'Could not retrieve Task: {0} v{1}'.format(
                    row[columns.get_loc('Task')],
                    row[columns.get_loc('Version')],
                )
                raise ParseError(detail=error, code='bad_request')
        elif mode.lower() == 'create':
            try:
                instance = Workflow.objects.create(
                    label=label,
                    version=float(row[columns.get_loc('Version')])
                )
            except Exception:
                error = 'Could not create Task: {0} v{1}'.format(
                    row[columns.get_loc('Task')],
                    row[columns.get_loc('Version')],
                )
                raise ParseError(detail=error, code='bad_request')
        else:
            raise ParseError(detail='Mode: {0} not supported'.format(mode), code='bad_request')

        instance.task.clear()
        instance.task.add(*task_list)
        instance.save()
