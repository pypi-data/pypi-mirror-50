from functools import lru_cache

from v3_0.actions.action import Action
from v3_0.actions.delete_posts_action import DeletePostsAction
from v3_0.actions.rearrange.rearrange_action import RearrangeAction
from v3_0.actions.schedule.schedule_action import ScheduleAction
from v3_0.actions.stage.models.stages_factory import StagesFactory
from v3_0.actions.stage.stage_action import StageAction
from v3_0.actions.sync_posts_status_action import SyncPostsStatusAction
from v3_0.shared.helpers.singleton import Singleton


class ActionFactory(Singleton):
    @lru_cache()
    def stage(self) -> Action:
        return StageAction(StagesFactory.instance())

    @lru_cache()
    def schedule(self) -> Action:
        return ScheduleAction()

    @lru_cache()
    def rearrange(self) -> Action:
        return RearrangeAction()

    @lru_cache()
    def sync_posts_status(self) -> Action:
        return SyncPostsStatusAction()

    @lru_cache()
    def delete_posts(self) -> Action:
        return DeletePostsAction()
