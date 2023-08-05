from nlpaug.augmenter.audio import AudioAugmenter
from nlpaug.util import Action
import nlpaug.model.audio as nma


class CorpAug(AudioAugmenter):
    def __init__(self, sampling_rate, corp_range=(0.2, 0.8), corp_factor=2, name='Corp_Aug', verbose=0):
        """

        :param sampling_rate: sampling rate of input audio
        :param corp_range: Range of applying corp operation. Default value is (0.2, 0.8)
            It means that first 20% and last 20% of data will not be excluded from augment operation. Augment operation
            will be applied to clip of rest of 60% time.
        :param corp_factor: duration of corping period (in second)
            replaced by 0.
        """

        super().__init__(
            action=Action.SUBSTITUTE, name=name, verbose=verbose)
        self.model = self.get_model(sampling_rate, corp_range, corp_factor)

    def get_model(self, sampling_rate, corp_range, corp_factor):
        return nma.Mask(sampling_rate, corp_range, corp_factor)
