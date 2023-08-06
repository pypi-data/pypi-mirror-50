from logging import getLogger
from injector import singleton

from typing import Union
from typing import Optional

from gumo.core.injector import injector
from gumo.task.infrastructure.configuration import TaskConfiguration
from gumo.task.bind import task_bind


logger = getLogger('gumo.task')


class ConfigurationFactory:
    @classmethod
    def build(
            cls,
            default_queue_name: Optional[str] = None,
            use_local_task_emulator: Union[str, bool, None] = None
    ) -> TaskConfiguration:
        use_emulator = None

        if isinstance(use_local_task_emulator, bool):
            use_emulator = use_local_task_emulator
        elif isinstance(use_local_task_emulator, str):
            use_emulator = use_local_task_emulator.lower() in ['true', 'yes']

        return TaskConfiguration(
            default_queue_name=default_queue_name,
            use_local_task_emulator=use_emulator,
        )


def configure(
        default_queue_name: Optional[str] = None,
        use_local_task_emulator: Union[str, bool, None] = None
) -> TaskConfiguration:
    config = ConfigurationFactory.build(
        default_queue_name=default_queue_name,
        use_local_task_emulator=use_local_task_emulator,
    )
    logger.debug(f'Gumo.Task is configured, config={config}')

    injector.binder.bind(TaskConfiguration, to=config, scope=singleton)
    injector.binder.install(task_bind)

    return config


def get_config() -> TaskConfiguration:
    return injector.get(TaskConfiguration, scope=singleton)
