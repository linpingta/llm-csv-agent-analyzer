from base_task import BaseTask


class FundAnalyzeTask(BaseTask):
    def __init__(self, config):
        super(FundAnalyzeTask, self).__init__(config)

        self.name = "fund_analyze"

    def _preprocess_data(self, logger):
        pass
