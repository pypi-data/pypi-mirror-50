# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2016 CERN.
#
# INSPIRE is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""Models for crawler integration."""

from __future__ import absolute_import, print_function

from datetime import datetime

from enum import Enum

from invenio_db import db

from sqlalchemy_utils.types import ChoiceType, UUIDType
from sqlalchemy.orm.exc import NoResultFound

from invenio_workflows.models import WorkflowObjectModel

from .errors import CrawlerJobNotExistError


class JobStatus(Enum):
    """Constants for possible status of any given PID."""

    __order__ = 'PENDING RUNNING FINISHED UNKNOWN'

    PENDING = 'pending'
    RUNNING = 'running'
    ERROR = 'error'
    FINISHED = 'finished'
    UNKNOWN = ''

    def __init__(self, value):
        """Hack."""

    def __eq__(self, other):
        """Equality test."""
        return self.value == other

    def __str__(self):
        """Return its value."""
        return self.value


class CrawlerJob(db.Model):
    """Keeps track of submitted crawler jobs."""

    __tablename__ = 'crawler_job'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_id = db.Column(UUIDType, index=True)
    spider = db.Column(db.String(255), index=True)
    workflow = db.Column(db.String(255), index=True)
    results = db.Column(db.Text, nullable=True)
    status = db.Column(ChoiceType(JobStatus, impl=db.String(10)),
                       nullable=False)
    logs = db.Column(db.Text, nullable=True)
    scheduled = db.Column(db.DateTime,
                          default=datetime.now,
                          nullable=False,
                          index=True)

    @classmethod
    def create(cls, job_id, spider, workflow, results=None,
               logs=None, status=JobStatus.PENDING):
        """Create a new entry for a scheduled crawler job."""
        obj = cls(
            job_id=job_id,
            spider=spider,
            workflow=workflow,
            results=results,
            logs=logs,
            status=status,
        )
        db.session.add(obj)
        return obj

    @classmethod
    def get_by_job(cls, job_id):
        """Get a row by Job UUID."""
        try:
            return cls.query.filter_by(
                job_id=job_id
            ).one()
        except NoResultFound:
            raise CrawlerJobNotExistError(job_id)

    def save(self):
        """Save object to persistent storage."""
        with db.session.begin_nested():
            db.session.add(self)


class CrawlerWorkflowObject(db.Model):
    """Relation between a job and workflow objects."""

    __tablename__ = "crawler_workflows_object"

    job_id = db.Column(UUIDType, primary_key=True)
    object_id = db.Column(
        db.Integer,
        db.ForeignKey(
            WorkflowObjectModel.id,
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        primary_key=True
    )


__all__ = (
    'CrawlerJob',
    'CrawlerWorkflowObject',
)
