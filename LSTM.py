import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import time
import sys

count = 20
OpenNMT = 0
cuda = False
train = False
if 'cuda' in sys.argv:
    cuda = True
if 'train' in sys.argv:
    train = True

#if OpenNMT == 1:
sizes = [[64,15,500,500],
         [64,20,500,500],
         [64,25,500,500],
         [64,30,500,500],
         [64,35,500,500],
         [64,40,500,500],
         [64,45,500,500],
         [64,50,500,500],
         [16,25,512,512],
         [32,25,512,512],
         [64,25,512,512],
         [128,25,512,512],
         [16,25,1024,1024],
         [32,25,1024,1024],
         [64,25,1024,1024],
         [128,25,1024,1024],
         [16,25,2048,2048],
         [32,25,2048,2048],
         [64,25,2048,2048],
         [128,25,2048,2048],
         [16,25,4096,4096],
         [32,25,4096,4096],
         [64,25,4096,4096],
         [128,25,4096,4096],
         [64,50,500,500]
        ]


for idx in range(len(sizes)):
  size = sizes[idx]
  N = size[0]
  T = size[1]
  D = size[2]
  H = size[3]
  
  if cuda:
    rnn = nn.LSTM(D,H,1).cuda()
    input = Variable(torch.randn(N, T, D).cuda())
    h0 = Variable(torch.randn(1, T, H).cuda())
    c0 = Variable(torch.randn(1, T, H).cuda())
  else:
    rnn = nn.LSTM(D,H,1)
    input = Variable(torch.randn(N, T, D))
    h0 = Variable(torch.randn(1, T, H))
    c0 = Variable(torch.randn(1, T, H))
  output, hn = rnn(input, (h0, c0))
  if train:
    loss_fn = nn.MSELoss().cuda()
  start = time.time()
  for j in range(count):
    output, hn = rnn(input, (h0, c0))
    if train:
      if cuda:
        targets = Variable(torch.randn(N,T,D).cuda())
      else:
        targets = Variable(torch.randn(N,T,D))
      loss = loss_fn(output,targets)
      loss.backward()
      if cuda:
        torch.cuda.synchronize()
  dura = (time.time() - start)/count
  gflops = T*4*(N*H*D*2 + N*H*H*2)/1e9
  GFLOPS = gflops/dura
  SPS = N/dura
  print("size = %s, duration = %.4f, gflops = %.4f, GFLOPS = %.4f, SPS = %.4f" %(size,dura,gflops,GFLOPS,SPS))