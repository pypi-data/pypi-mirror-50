"""
    FCN, implemented in Gluon.
    Original paper: 'Fully Convolutional Networks for Semantic Segmentation,' https://arxiv.org/abs/1411.4038.
"""

__all__ = ['FCN', 'fcn_resnet50_voc', 'fcn_resnet101_voc', 'fcn_resnet50_ade20k']

import os
from mxnet import cpu
from mxnet.gluon import nn, HybridBlock
from .common import conv1x1, conv3x3_block
from .resnet import resnet50, resnet101


class FCN(HybridBlock):
    """
    FCN model from 'Fully Convolutional Networks for Semantic Segmentation,' https://arxiv.org/abs/1411.4038.

    Parameters:
    ----------
    backbone : nn.Sequential
        Feature extractor.
    backbone_out_channels : int, default 2048
        Number of output channels form feature extractor.
    in_channels : int, default 3
        Number of input channels.
    in_size : tuple of two ints, default (224, 224)
        Spatial size of the expected input image.
    classes : int, default 21
        Number of segmentation classes.
    """
    def __init__(self,
                 backbone,
                 backbone_out_channels=2048,
                 in_channels=3,
                 in_size=(224, 224),
                 classes=21,
                 **kwargs):
        super(FCN, self).__init__(**kwargs)
        assert (in_channels > 0)
        self.in_size = in_size
        self.classes = classes
        mid_channels = backbone_out_channels // 4

        with self.name_scope():
            self.backbone = backbone
            self.conv1 = conv3x3_block(
                in_channels=backbone_out_channels,
                out_channels=mid_channels)
            self.dropout = nn.Dropout(rate=0.1)
            self.conv2 = conv1x1(
                in_channels=mid_channels,
                out_channels=classes)

    def hybrid_forward(self, F, x):
        x = self.backbone(x)
        x = self.conv1(x)
        x = self.dropout(x)
        x = self.conv2(x)
        x = F.contrib.BilinearResize2D(x, height=self.in_size[0], width=self.in_size[1])
        return x


def get_fcn(backbone,
            num_classes,
            model_name=None,
            pretrained=False,
            ctx=cpu(),
            root=os.path.join('~', '.mxnet', 'models'),
            **kwargs):
    """
    Create FCN model with specific parameters.

    Parameters:
    ----------
    backbone : nn.Sequential
        Feature extractor.
    num_classes : int
        Number of segmentation classes.
    model_name : str or None, default None
        Model name for loading pretrained model.
    pretrained : bool, default False
        Whether to load the pretrained weights for model.
    ctx : Context, default CPU
        The context in which to load the pretrained weights.
    root : str, default '~/.mxnet/models'
        Location for keeping the model parameters.
    """

    net = FCN(
        backbone=backbone,
        classes=num_classes,
        **kwargs)

    if pretrained:
        if (model_name is None) or (not model_name):
            raise ValueError("Parameter `model_name` should be properly initialized for loading pretrained model.")
        from .model_store import get_model_file
        net.load_parameters(
            filename=get_model_file(
                model_name=model_name,
                local_model_store_dir_path=root),
            ctx=ctx)

    return net


def fcn_resnet50_voc(pretrained_backbone=False, num_classes=21, **kwargs):
    """
    FCN model on the base of ResNet-50 for Pascal VOC from 'Fully Convolutional Networks for Semantic Segmentation,'
    https://arxiv.org/abs/1411.4038.

    Parameters:
    ----------
    pretrained_backbone : bool, default False
        Whether to load the pretrained weights for feature extractor.
    num_classes : int, default 21
        Number of segmentation classes.
    pretrained : bool, default False
        Whether to load the pretrained weights for model.
    ctx : Context, default CPU
        The context in which to load the pretrained weights.
    root : str, default '~/.mxnet/models'
        Location for keeping the model parameters.
    """
    backbone = resnet50(pretrained=pretrained_backbone, dilated=True).features[:-1]
    return get_fcn(backbone=backbone, num_classes=num_classes, model_name="fcn_resnet50_voc", **kwargs)


def fcn_resnet101_voc(pretrained_backbone=False, num_classes=21, **kwargs):
    """
    FCN model on the base of ResNet-101 for Pascal VOC from 'Fully Convolutional Networks for Semantic Segmentation,'
    https://arxiv.org/abs/1411.4038.

    Parameters:
    ----------
    pretrained_backbone : bool, default False
        Whether to load the pretrained weights for feature extractor.
    num_classes : int, default 21
        Number of segmentation classes.
    pretrained : bool, default False
        Whether to load the pretrained weights for model.
    ctx : Context, default CPU
        The context in which to load the pretrained weights.
    root : str, default '~/.mxnet/models'
        Location for keeping the model parameters.
    """
    backbone = resnet101(pretrained=pretrained_backbone, dilated=True).features[:-1]
    return get_fcn(backbone=backbone, num_classes=num_classes, model_name="fcn_resnet101_voc", **kwargs)


def fcn_resnet50_ade20k(pretrained_backbone=False, num_classes=150, **kwargs):
    """
    FCN model on the base of ResNet-50 for ADE20K from 'Fully Convolutional Networks for Semantic Segmentation,'
    https://arxiv.org/abs/1411.4038.

    Parameters:
    ----------
    pretrained_backbone : bool, default False
        Whether to load the pretrained weights for feature extractor.
    num_classes : int, default 150
        Number of segmentation classes.
    pretrained : bool, default False
        Whether to load the pretrained weights for model.
    ctx : Context, default CPU
        The context in which to load the pretrained weights.
    root : str, default '~/.mxnet/models'
        Location for keeping the model parameters.
    """
    backbone = resnet50(pretrained=pretrained_backbone, dilated=True).features[:-1]
    return get_fcn(backbone=backbone, num_classes=num_classes, model_name="fcn_resnet50_ade20k", **kwargs)


def _test():
    import numpy as np
    import mxnet as mx

    pretrained = False

    models = [
        (fcn_resnet50_voc, 21),
        (fcn_resnet101_voc, 21),
        (fcn_resnet50_ade20k, 150),
    ]

    for model, classes in models:

        net = model(pretrained=pretrained)

        ctx = mx.cpu()
        if not pretrained:
            net.initialize(ctx=ctx)

        # net.hybridize()
        net_params = net.collect_params()
        weight_count = 0
        for param in net_params.values():
            if (param.shape is None) or (not param._differentiable):
                continue
            weight_count += np.prod(param.shape)
        print("m={}, {}".format(model.__name__, weight_count))
        assert (model != fcn_resnet50_voc or weight_count == 32956992)
        assert (model != fcn_resnet101_voc or weight_count == 51949120)
        assert (model != fcn_resnet50_ade20k or weight_count == 33023040)

        x = mx.nd.zeros((1, 3, 224, 224), ctx=ctx)
        y = net(x)
        assert ((y.shape[0] == x.shape[0]) and (y.shape[1] == classes) and (y.shape[2] == x.shape[2]) and
                (y.shape[3] == x.shape[3]))


if __name__ == "__main__":
    _test()
