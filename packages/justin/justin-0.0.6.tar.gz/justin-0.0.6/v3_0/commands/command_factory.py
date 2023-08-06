from functools import lru_cache
from typing import List

from v3_0.commands.command import Command
from v3_0.commands.delete_posts_command import DeletePostsCommand
from v3_0.commands.schedule_command import ScheduleCommand
from v3_0.commands.stage_command import StageCommand
from v3_0.actions.stage.models.stages_factory import StagesFactory


class CommandFactory:
    @staticmethod
    @lru_cache()
    def instance() -> 'CommandFactory':
        return CommandFactory()

    @lru_cache()
    def commands(self) -> List[Command]:
        return [
            self.stage(),
            self.schedule(),
            self.delete_posts()
        ]

    @lru_cache()
    def stage(self) -> Command:
        return StageCommand(StagesFactory.instance())

    @lru_cache()
    def schedule(self) -> Command:
        return ScheduleCommand()

    @lru_cache()
    def delete_posts(self) -> Command:
        return DeletePostsCommand()
