from .base_task import BaseTask


class EstateAnalyzeTask(BaseTask):
    def __init__(self, config):
        super(EstateAnalyzeTask, self).__init__(config)

        self.name = "estate_analyze"

    def _preprocess_data(self, logger):
        pass

    def inference(self, question, logger):
        pass
