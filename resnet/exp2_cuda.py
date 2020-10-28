'''Train CIFAR-10 with PyTorch.'''
# -*- coding: UTF-8 -*-
import os

import torch
import torch.backends.cudnn as cudnn
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, TensorDataset
import torchvision
import torchvision.transforms as transforms
import pickle
from models import resnet20

with open('traindata_n.p', 'rb') as fin:
	traindata = pickle.load(fin)
with open('traintag_n.p', 'rb') as fin:
	traintag = pickle.load(fin)
'''
x_data = torch.from_numpy(traindata[:,0:-1])
y_data = torch.from_numpy(traindata[:,[-1]])
dataset = TensorDataset(x_data, y_data)
'''


class DealDataset(Dataset):

	def __init__(self, x, y):
		self.x_data = torch.from_numpy(x)
		self.y_data = torch.from_numpy(y)
		self.len = x.shape[0]

	def __getitem__(self, index):
		return self.x_data[index], self.y_data[index]

	def __len__(self):
		return self.len

dataset = DealDataset(traindata, traintag)

start_epoch = 700
end_epoch = 2000
lr = 0.001

# Data pre-processing, DO NOT MODIFY
print('==> Preparing data..')
transform_train = transforms.Compose([
	transforms.RandomCrop(32, padding=4),
	transforms.RandomHorizontalFlip(),
	transforms.ToTensor(),
	transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
])

transform_test = transforms.Compose([
	transforms.ToTensor(),
	transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
])

trainset = torchvision.datasets.CIFAR10(
	root='./data', train=True, download=True, transform=transform_train)
#print(type(trainset))
#print(trainset)

trainloader = torch.utils.data.DataLoader(dataset, batch_size=512, shuffle=True)

testset = torchvision.datasets.CIFAR10(
	root='./data', train=False, download=True, transform=transform_test)
testloader = torch.utils.data.DataLoader(dataset, batch_size=512, shuffle=False)

classes = ('huawei', 'xiaomi', 'oppo', 'vivo', 'sumsung')

# Model
print('==> Building model..')
model = resnet20(45)
# If you want to restore training (instead of training from beginning),
# you can continue training based on previously-saved models
# by uncommenting the following two lines.
# Do not forget to modify start_epoch and end_epoch.

restore_model_path = 'checkpoint/ckpt_699_acc_0.547307.pth'
model.load_state_dict(torch.load(restore_model_path)['net'])

# A better method to calculate loss
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=lr, weight_decay=5e-4)

model.cuda()
criterion.cuda()

def train(epoch):
	model.train()
	train_loss = 0
	correct = 0
	total = 0
	for batch_idx, (inputs, targets) in enumerate(trainloader):
		inputs = inputs.cuda()
		targets = targets.cuda()
		optimizer.zero_grad()
		#print(inputs.shape)
		#print(targets.shape)
		outputs = model(inputs)
		# The outputs are of size [128x10].
		# 128 is the number of images fed into the model 
		# (yes, we feed a certain number of images into the model at the same time, 
		# instead of one by one)
		# For each image, its output is of length 10.
		# Index i of the highest number suggests that the prediction is classes[i].
		#print(outputs)
		#print(outputs.shape)
		#print(targets)
		#print(targets.shape)
		loss = criterion(outputs, targets)
		loss.backward()
		optimizer.step()
		train_loss += loss.item()
		_, predicted = outputs.max(1)
		total += targets.size(0)
		correct += predicted.eq(targets).sum().item()
		print('Epoch [%d] Batch [%d/%d] Loss: %.3f | Traininig Acc: %.3f%% (%d/%d)'
			  % (epoch, batch_idx + 1, len(trainloader), train_loss / (batch_idx + 1),
				 100. * correct / total, correct, total))
	with open('ACC.report', 'a') as fout:
		fout.write('EPOCH {}: TRAIN ACC {}%\n'.format(epoch, 100. * correct / total))


def test(epoch):
	print('==> Testing...')
	model.eval()
	total = 0
	correct = 0
	with torch.no_grad():
		for batch_idx, (inputs, targets) in enumerate(testloader):
			inputs = inputs.cuda()
			targets = targets.cuda()
			outputs = model(inputs)
			#print('outputs', outputs)
			_, predicted = outputs.max(1)
			print(predicted)
			#print('predicted', predicted)
			total += targets.size(0)
			#print('targets', targets)
			#print('eq', predicted.eq(targets), predicted.eq(targets).sum(), predicted.eq(targets).sum().item())
			correct += predicted.eq(targets).sum().item()
		########################################

	# Save checkpoint.
	acc = 1. * correct / total
	print('Test Acc: %f' %acc)
	with open('ACC.report', 'a') as fout:
		fout.write('EPOCH {}: TEST ACC {}%\n'.format(epoch, 100. * acc))
	print('Saving..')
	state = {
		'net': model.state_dict(),
		'acc': acc,
		'epoch': epoch,
	}
	if not os.path.isdir('checkpoint'):
		os.mkdir('checkpoint')
	torch.save(state, './checkpoint/ckpt_%d_acc_%f.pth' % (epoch, acc))


for epoch in range(start_epoch, end_epoch + 1):
	train(epoch)
	if epoch % 10 == 9:
		test(epoch)

