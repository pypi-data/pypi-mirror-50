from argparse import Namespace

from pyvko.models.group import Group

from v3_0.actions.action import Action
from v3_0.actions.stage.exceptions.check_failed_error import CheckFailedError
from v3_0.actions.stage.logic.exceptions.extractor_error import ExtractorError
from v3_0.actions.stage.models.stage import Stage
from v3_0.actions.stage.models.stages_factory import StagesFactory
from v3_0.shared.models.photoset import Photoset
from v3_0.shared.models.world import World


class StageAction(Action):
    def __init__(self, factory: StagesFactory) -> None:
        super().__init__()

        self.__stages_factory = factory

    def perform(self, args: Namespace, world: World, group: Group) -> None:

        # check if able to exit
        # cleanup
        # check if able to enter
        # move
        # prepare

        new_stage: Stage = args.new_stage

        for photoset_name in args.name:
            photosets = world[photoset_name]

            photoset = photosets[0]

            current_stage = self.__stages_factory.stage_by_path(photoset.path)

            assert isinstance(photoset, Photoset)

            print(f"Trying to move \"{photoset.name}\" to stage \"{new_stage.name}\"")

            transfer_checks = current_stage.outcoming_checks + new_stage.incoming_checks

            try:
                current_stage.cleanup(photoset)

                for check in transfer_checks:
                    check.rollback(photoset)

                print("Running checks")

                for check in transfer_checks:
                    print(f"Running {check.name} for {photoset.name}... ", end="")

                    result = check.is_good(photoset)

                    if result:
                        print("passed")
                    else:
                        print("not passed")

                        if check.ask_for_extract():
                            check.extract(photoset)

                        raise CheckFailedError(f"Failed {check.name}")

                if new_stage != current_stage:
                    new_stage.transfer(photoset)

                new_stage.prepare(photoset)
            except (ExtractorError, CheckFailedError) as error:
                print(f"Unable to {new_stage.name} {photoset.name}: {error}")
            else:
                print("Moved successfully")
