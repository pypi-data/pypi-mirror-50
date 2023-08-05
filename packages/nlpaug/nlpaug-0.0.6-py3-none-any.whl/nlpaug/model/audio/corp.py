import numpy as np

from nlpaug.model.audio import Audio


class Corp(Audio):
    def __init__(self, sampling_rate, corp_range=(0.2, 0.8), corp_factor=2):
        """

        :param sampling_rate: sampling rate of input audio
        :param corp_range: Range of applying corp operation. Default value is (0.2, 0.8)
            It means that first 20% and last 20% of data will not be excluded from augment operation. Augment operation
            will be applied to clip of rest of 60% time.
        :param corp_factor: duration of corping period (in second)
            replaced by 0.
        """
        super().__init__()
        self.sampling_rate = sampling_rate
        self.corp_range = corp_range
        self.corp_factor = corp_factor

    def manipulate(self, data):
        valid_region = (int(len(data) * self.corp_range[0]), int(len(data) * self.corp_range[1]))

        start_timeframe = np.random.randint(valid_region[0], valid_region[1])
        end_timeframe = start_timeframe + self.sampling_rate * self.corp_factor

        augmented_data = data.copy()
        np.delete(augmented_data, np.s_[start_timeframe:end_timeframe])

        return augmented_data
