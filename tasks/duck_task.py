from .base_task import BaseTask


class DuckTask(BaseTask):
    def __init__(self, config):
        super(DuckTask, self).__init__(config)

        self.name = "duck"

    def _preprocess_data(self, logger):
        pass

    def inference(self, answer, logger):
        logger.info("duck task with answer[%s]" % answer)
