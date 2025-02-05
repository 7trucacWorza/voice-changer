from torch import device

from const import EmbedderType
from voice_changer.RVC.embedder.Embedder import Embedder
from voice_changer.RVC.embedder.FairseqContentvec import FairseqContentvec
from voice_changer.RVC.embedder.FairseqHubert import FairseqHubert
from voice_changer.RVC.embedder.FairseqHubertJp import FairseqHubertJp
from voice_changer.utils.VoiceChangerParams import VoiceChangerParams


class EmbedderManager:
    currentEmbedder: Embedder | None = None
    params: VoiceChangerParams

    @classmethod
    def initialize(cls, params: VoiceChangerParams):
        cls.params = params

    @classmethod
    def getEmbedder(
        cls, embederType: EmbedderType, isHalf: bool, dev: device
    ) -> Embedder:
        if cls.currentEmbedder is None:
            print("[Voice Changer] generate new embedder. (no embedder)")
            cls.currentEmbedder = cls.loadEmbedder(embederType, isHalf, dev)
        elif cls.currentEmbedder.matchCondition(embederType) is False:
            print("[Voice Changer] generate new embedder. (not match)")
            cls.currentEmbedder = cls.loadEmbedder(embederType, isHalf, dev)
        else:
            cls.currentEmbedder.setDevice(dev)
            cls.currentEmbedder.setHalf(isHalf)
            # print("[Voice Changer] generate new embedder. (ANYWAY)", isHalf)
            # cls.currentEmbedder = cls.loadEmbedder(embederType, file, isHalf, dev)
        return cls.currentEmbedder

    @classmethod
    def loadEmbedder(
        cls, embederType: EmbedderType, isHalf: bool, dev: device
    ) -> Embedder:
        if embederType == "hubert_base":
            file = cls.params.hubert_base
            return FairseqHubert().loadModel(file, dev, isHalf)
        elif embederType == "hubert-base-japanese":
            file = cls.params.hubert_base_jp
            return FairseqHubertJp().loadModel(file, dev, isHalf)
        elif embederType == "contentvec":
            file = cls.params.hubert_base
            return FairseqContentvec().loadModel(file, dev, isHalf)
        else:
            return FairseqHubert().loadModel(file, dev, isHalf)
