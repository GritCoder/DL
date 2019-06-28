import sys
#import caffe
import argparse
import os
from collections import OrderedDict
import torch.nn as nn
import torch.nn.functional as F
import torch
import numpy as np
from torch.autograd import Variable
#from prototxt2 import *
#from pytorch2caffe2 import pytorch2caffe
import torchvision
from model.build_BiSeNet import BiSeNet
import torch.onnx

print(torch.__file__)
def main(num_classes, context_path, check_points):
    os.environ['CUDA_VISIBLE_DEVICES'] = '7'
    model = BiSeNet(num_classes, context_path).cuda()
    #if torch.cuda.is_available():
    #model.load_state_dict(torch.load(check_points))
    #model = torch.nn.DataParallel(model).cuda()
    #model.load_state_dict(torch.load(check_points))
    # load pretrained model if exists
    #model.eval()
    # load pretrained model if exists
    #print('load model from %s ...' % check_points)
    #model.load_state_dict(torch.load(check_points))
    print('load model from %s ...' % check_points)
    model.load_state_dict(torch.load(check_points))
    print('load model success')
    
    input_var = torch.randn(1, 3, 480, 640, device='cuda')
    #output_var = model(input_var)
    input_names=["input1"]
    output_names=["output1"]   
    torch.onnx.export(model,input_var,'Bisenet_nearest.onnx',verbose = True, input_names = input_names, output_names = output_names)
    #example = torch.rand(1, 3, 640, 640)
    #traced_script_module = torch.jit.trace(model, example)
    #traced_script_module.save('BIS18.pt')
    #torch.onnx.export(model,input_var,"BiSeNet.proto",verbose = True)
    #from mmdnn.conversion.pytorch.pytorch_parser import PytorchParser
    #pytorchparser = PytorchParser(model, [3,640,640])
    #IR_FILE = 'BiSeNet'
    #pytorchparser.run(IR_FILE)
    #input_var = Variable(torch.randn(1, 3, 640, 640))
    #output_var = model(input_var)
    #torch.onnx.export(model,input_var,'BiSeNet.proto',verbose = True)
    #pytorch2caffe(input_var, output_var, 'BiSeNet-pytorch2caffe.prototxt', 'BiSeNet-pytorch2caffe.caffemodel')

main(int(2),str('resnet101'),'/home/sshengli/Pytorch/BiSeNet_lxf/BiSeNet/nearest_checkpoints_101_adam/epoch_150.pth')


