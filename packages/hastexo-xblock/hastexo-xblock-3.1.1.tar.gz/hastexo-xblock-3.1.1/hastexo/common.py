import sys

from django.conf import settings as django_settings

from .models import Stack


CREATE_STATE = 'CREATE_COMPLETE'
RESUME_STATE = 'RESUME_COMPLETE'
UPDATE_STATE = 'UPDATE_COMPLETE'
ROLLBACK_STATE = 'ROLLBACK_COMPLETE'
SNAPSHOT_STATE = 'SNAPSHOT_COMPLETE'
LAUNCH_STATE = 'LAUNCH_PENDING'
LAUNCH_ERROR_STATE = 'LAUNCH_ERROR'
SUSPEND_STATE = 'SUSPEND_PENDING'
SUSPEND_FAILED_STATE = 'SUSPEND_FAILED'
SUSPEND_ISSUED_STATE = 'SUSPEND_ISSUED'
SUSPEND_RETRY_STATE = 'SUSPEND_RETRY'
RESUME_IN_PROGRESS_STATE = 'RESUME_IN_PROGRESS'
RESUME_FAILED_STATE = 'RESUME_FAILED'
DELETED_STATE = 'DELETE_COMPLETE'
DELETE_STATE = 'DELETE_PENDING'
DELETE_IN_PROGRESS_STATE = 'DELETE_IN_PROGRESS'
DELETE_FAILED_STATE = 'DELETE_FAILED'

UP_STATES = (
    CREATE_STATE,
    RESUME_STATE,
    UPDATE_STATE,
    ROLLBACK_STATE,
    SNAPSHOT_STATE
)

OCCUPANCY_STATES = (
    CREATE_STATE,
    RESUME_STATE,
    UPDATE_STATE,
    ROLLBACK_STATE,
    SNAPSHOT_STATE,
    LAUNCH_STATE,
    SUSPEND_STATE,
    SUSPEND_ISSUED_STATE,
    SUSPEND_RETRY_STATE
)

SETTINGS_KEY = 'hastexo'

DEFAULT_SETTINGS = {
    "terminal_url": "/hastexo-xblock/",
    "launch_timeout": 900,
    "suspend_timeout": 120,
    "suspend_interval": 60,
    "suspend_concurrency": 4,
    "check_timeout": 120,
    "delete_age": 14,
    "delete_attempts": 3,
    "delete_interval": 86400,
    "task_timeouts": {
        "sleep": 10,
        "retries": 90
    },
    "js_timeouts": {
        "status": 15000,
        "keepalive": 30000,
        "idle": 3600000,
        "check": 5000
    },
    "providers": {}
}


if sys.version_info < (3,):
    def b(x):
        return x
else:
    import codecs

    def b(x):
        return codecs.latin_1_encode(x)[0]


def get_xblock_settings():
    try:
        xblock_settings = django_settings.XBLOCK_SETTINGS
    except AttributeError:
        settings = DEFAULT_SETTINGS
    else:
        settings = xblock_settings.get(
            SETTINGS_KEY, DEFAULT_SETTINGS)

    return settings


def update_stack(name, course_id, student_id, data):
    stack = Stack.objects.get(
        student_id=student_id,
        course_id=course_id,
        name=name
    )
    update_stack_fields(stack, data)
    stack.save(update_fields=list(data.keys()))


def update_stack_fields(stack, data):
    for field, value in data.items():
        if hasattr(stack, field):
            setattr(stack, field, value)


def get_stack(name, course_id, student_id, prop=None):
    stack = Stack.objects.get(
        student_id=student_id,
        course_id=course_id,
        name=name
    )

    if prop:
        return getattr(stack, prop)
    else:
        return stack
