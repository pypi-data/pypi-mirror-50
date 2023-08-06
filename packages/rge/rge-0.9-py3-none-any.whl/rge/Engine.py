import os
import os.path
from os import path
import nltk, collections

import sys
import json
import random 

import numpy as np
from tqdm import tqdm
from itertools import chain
import matplotlib.pyplot as plt

# from src.Train import test, train
# from src.utils. import AverageMeter
from rge.Train import test,train
from colorama import init 
from termcolor import colored 
from rge.utils import (AverageMeter, save_checkpoint,get_text)
import torch 
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision.utils import save_image
import fileinput
import time  
from torchvision import transforms
import importlib.util
from importlib.machinery import SourceFileLoader

DIR_DATA = ''

class Engine(object):
    def __init__ (self, dir, hot_start, full_diagnostic, cuda):
        global DIR_DATA

        # parser.add_argument('dir', type=str, help="directory of config file")
        # parser.add_argument('--full_diagnostic', type=str, help="run full diagnostic (print) [default: false]", default=False)


        # parser.add_argument('--dir', type=int, help="directory of config file" default="data/data.json")
        # .add_argument('--cuda', action='store_true', help='Enable cuda')
        self.dir = dir
        self.config = self.dir
        self.parsed = {}
        with open(self.config) as f:
            self.parsed = json.load(f)
        self.gpu = self.parsed['gpu']
        self.dir_data_config = self.parsed['dir']
        DIR = self.dir_data_config

        self.time = 0
        cuda = cuda and torch.cuda.is_available()
        self.fd = full_diagnostic
        self.device = torch.device('cuda:'+ self.gpu if cuda else 'cpu')
        self.image_transforms = transforms.Resize(32)

        # get rid of extra spaces

        self.loss = None
        self.accuracy = None
        if (self.fd):
            print(" ")
            print(colored("==begining data (args put in)==", 'magenta'))
            print(colored("Directory: "+ self.dir, 'cyan'))
            print(colored("==ending data (args put in)==", 'magenta'))
            print(" ")


        
            # print(self.parsed)

        assert self.parsed
        self.seed = self.parsed['seed']
        
        seedNew = random.randint(1,1000001)
        self.seed = seedNew 
        self.out_dir = self.parsed['out_dir']
        DIR_DATA = self.out_dir

        if not os.path.exists(DIR + 'seeds_save/'):
            os.makedirs(DIR + 'seeds_save/')
        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)

        if path.exists(DIR+ 'seeds_save/' + 'seed.txt'):
            # val.write(str(val.read()) + "\n" + str(seedNew))
            
            with open(DIR+ 'seeds_save/' + 'seed.txt','a') as f:
                f.write('\n' + str(self.seed))
                f.flush()
        else:
            completeName = os.path.join(DIR + 'seeds_save/' + 'seed.txt')         
            file1 = open(completeName, "w")
            file1.write(str(self.seed))
            file1.close()



        torch.manual_seed(self.seed)
        np.random.seed(self.seed)

        self.name = self.parsed['name']
        self.modelDir = self.parsed['model'][0]
        self.trainDir = self.parsed['training'][0]
        
        # self.bi = self.modelDir['bidir']
        self.distance = self.modelDir['dis']
        self.class_name = self.modelDir['class_name']
        self.type = self.modelDir['type']
        self.file_path = self.modelDir['file_path']


        if self.type == "Color":
            from rge.datasets.ColorDataset import (ReferenceGame)
        elif self.type == "Chair":
            from rge.datasets.ChairDataset import (ReferenceGame)
        elif self.type == "Creatures":
            from rge.datasets.CreaturesDataset import (ReferenceGame)
        
        


        name = os.path.basename(self.file_path)
        f_path = self.file_path.replace(name,"")
        name = name.replace('.py','')


        sys.path.append(os.path.dirname(f_path))

        module = __import__(name)
        

        while (os.path.dirname(f_path) in sys.path):    
            sys.path.remove(os.path.dirname(f_path))
        
        sup = getattr(module, self.class_name)

        # get rid of commented out things unless important

        #module = __import__(module_name)
        #class_ = getattr(module, class_name)
        #instance = class_()
        # breakpoint()
        # split = self.file_path.split('/', 0)
        # name = os.path.basename(self.file_path)
        # f_path = self.file_path.replace(name,"")

        # sys.path.append(os.path.dirname(f_path))
        # module = __import__(name)
        # sup = getattr(module, self.class_name)

        self.lr = self.trainDir['learning_rate']
        #self.num = self.trainDir['number']
        #self.width = self.trainDir['width']

        self.bs = self.trainDir['batch_size']
        self.epochs = self.trainDir['epochs']
        self.dim = self.trainDir['dim']
        self.log_interval = self.trainDir['log_interval']


        # pylint to make nice indents
        self.train_dataset = ReferenceGame('Train', context_condition=self.distance, image_transform=self.image_transforms)
        #self.dataTrain = self.train_dataset.data
        self.train_loader = DataLoader(self.train_dataset, shuffle=True, batch_size=self.bs)
        self.N_mini_batches = len(self.train_loader)
        self.vocab_size = self.train_dataset.vocab_size
        self.vocab = self.train_dataset.vocab
        self.ref_dataset = ReferenceGame('Test', vocab=self.vocab, context_condition=self.distance,image_transform=self.image_transforms)
        #self.dataRef = self.ref_dataset.data
        self.test_dataset = ReferenceGame('Validation', vocab=self.vocab, context_condition=self.distance,image_transform=self.image_transforms)
        self.test_loader = DataLoader(self.test_dataset, shuffle=False, batch_size=self.bs)
        #self.dataTest = self.test_loader.data

        self.sup_img = sup(self.vocab_size, device=self.device).to(self.device)

        self.optimizer = torch.optim.Adam(
            chain(
                self.sup_img.parameters(),
            ), lr=self.lr)
        
        self.hot_start = hot_start
        if (self.hot_start != ""):
            checkpoint = torch.load(self.hot_start)
            self.hot_epoch = checkpoint['epoch']
            self.epochs = self.epochs - self.hot_epoch
            self.optimizer.load_state_dict(checkpoint['optimizer'])
            self.sup_img.load_state_dict(checkpoint['sup_img'])

        # model
        self.__init_model(self.config)
        if (self.fd):
            self.check_data()

        self.train()

        self.final_loss()
        self.final_accuracy()
        self.final_time()
        # self.final_perplexity()
        print(self.dir_data_config+'plot_data/' + 'plot_' + self.name + ".txt") 

        if path.exists(self.dir_data_config+'plot_data/' + 'plot_' + self.name + ".txt"):    
            with open(self.dir_data_config+'plot_data/' + 'plot_' + self.name + ".txt", 'a') as f:
                f.write('\n' + str(self.accuracy))
                f.flush()
        else:
            completeName = os.path.join(self.dir_data_config+'plot_data/' + 'plot_' + self.name + ".txt")         
            file1 = open(completeName, "w")
            file1.write(str(self.accuracy))
            file1.close()
        

    def __init_model(self, config):
        print("init model")
        #Model or Training class? Save to a self.var?
    
    def check_data(self):
        print(colored("==begining data (config)==", 'magenta'))
        print(colored("name: "+ self.name , 'cyan'))
        print(colored("Class Name: "+ self.class_name , 'cyan'))
        print(colored("learning rate: "+ str(self.lr) , 'cyan'))
        print(colored("batch size: "+ str(self.bs) , 'cyan'))
        print(colored("epochs: "+ str(self.epochs) , 'cyan'))
        print(colored("dim: "+ str(self.dim) , 'cyan'))
        print(colored("log interval: "+ str(self.log_interval) , 'cyan'))
        print(colored("==ending data (config)==", 'magenta'))
        print(" ")

    def train(self):
        best_loss = float('inf')
        track_loss = np.zeros((self.epochs, 2))
        t0 = time.time()
        
        for epoch in range(1, self.epochs + 1):
            if (self.hot_start != ""):
                epoch = epoch + self.hot_epoch - 1
            t_loss = self.train_one_epoch(epoch)
            v_loss = self.validate_one_epoch(epoch)

            is_best = v_loss < best_loss
            best_loss = min(v_loss, best_loss)
            track_loss[epoch - 1, 0] = t_loss
            track_loss[epoch - 1, 1] = v_loss
            # print("dict; " + str(self.optimizer.state_dict()))
            # print("dict-none; " + str(self.optimizer))

            save_checkpoint({
                'epoch': epoch,
                'sup_img': self.sup_img.state_dict(),
                'track_loss': track_loss,
                'optimizer': self.optimizer.state_dict(),
                'vocab': self.vocab,
                'vocab_size': self.vocab_size,
            }, is_best, folder=DIR_DATA)
            np.save(os.path.join(DIR_DATA, 'loss.npy'), track_loss)
        self.time = time.time() - t0
    
    def train_one_epoch(self, epoch): 
        #train a single epoch 

        train_loss = train(epoch,self.sup_img,self.train_loader,self.device,self.optimizer)
        return train_loss

    def validate_one_epoch(self, epoch): 
        # validate a single epoch 
        test_loss = test(epoch,self.sup_img,self.test_loader,self.device,self.optimizer)
        return test_loss

    def final_accuracy(self):
        ref_loader = DataLoader(self.ref_dataset, shuffle=False, batch_size=self.bs)
        N_mini_batches = len(ref_loader)
        with torch.no_grad():

            total_count = 0
            correct_count = 0
            correct = False
            
            for batch_idx, (tgt_rgb, d1_rgb, d2_rgb, x_inp, x_len) in enumerate(ref_loader):
                batch_size = x_inp.size(0)
                tgt_rgb = tgt_rgb.to(self.device).float()
                d1_rgb = d1_rgb.to(self.device).float()
                d2_rgb = d2_rgb.to(self.device).float()
                x_inp = x_inp.to(self.device)
                x_len = x_len.to(self.device)

                tgt_score = self.sup_img(tgt_rgb, x_inp, x_len)
                d1_score = self.sup_img(d1_rgb, x_inp, x_len)
                d2_score = self.sup_img(d2_rgb, x_inp, x_len)
                soft = nn.Softmax(dim=1)
                loss = soft(torch.cat([tgt_score,d1_score,d2_score],1))
                softList = torch.argmax(loss, dim=1)

                correct_count += torch.sum(softList == 0).item()
                total_count += softList.size(0)
                

            accuracy = correct_count / float(total_count) * 100
            # print('====> Final Test Loss: {:.4f}'.format(loss_meter.avg))
            print(colored("==begining data (final accuracy)==", 'magenta'))
            print(colored('====> Final Accuracy: {}/{} = {}%'.format(correct_count, total_count, accuracy), 'cyan'))
            print(colored("==ending data (final accuracy)==", 'magenta'))
            print("")
            self.accuracy = accuracy

    def final_loss(self):
        print(colored("==begining data (final loss)==", 'magenta'))
        test_loader = DataLoader(self.test_dataset, shuffle=True, batch_size=self.bs)
        N_mini_batches = len(test_loader)
        with torch.no_grad():
            loss_meter = AverageMeter()

            for batch_idx, (tgt_rgb, d1_rgb, d2_rgb, x_inp, x_len) in enumerate(test_loader):
                batch_size = x_inp.size(0)
                tgt_rgb = tgt_rgb.to(self.device).float()
                d1_rgb = d1_rgb.to(self.device).float()
                d2_rgb = d2_rgb.to(self.device).float()
                x_inp = x_inp.to(self.device)
                x_len = x_len.to(self.device)

                # obtain predicted rgb
                tgt_score = self.sup_img(tgt_rgb, x_inp, x_len)
                d1_score = self.sup_img(d1_rgb, x_inp, x_len)
                d2_score = self.sup_img(d2_rgb, x_inp, x_len)

                loss = F.cross_entropy(torch.cat([tgt_score,d1_score,d2_score], 1), torch.LongTensor(np.zeros(batch_size)).to(self.device))
                self.loss = loss
             
                loss_meter.update(loss.item(), batch_size)
            print(colored('====> Final Test Loss: {:.4f}'.format(loss_meter.avg),'cyan'))
            
        print(colored("==ending data (final loss)==", 'magenta'))
        print("")
    
    def final_time(self):
        print(colored("==begining data (final time)==", 'magenta'))
        print(colored('====> Final Time: {:.4f}'.format(self.time),'cyan'))
        print(colored("==ending data (final time)==", 'magenta'))
        print("")
    
    def final_perplexity(self):
        corpus = ""
        perp = 0
        counter = 0

        # for i in self.train_dataset.get_textColor():
        #     corpus = corpus + " " + i
        # for i in self.ref_dataset.get_textColor():
        #     corpus = corpus + " " + i
        # for i in self.test_dataset.get_textColor():
        #     corpus = corpus + " " + i

        # print(corpus)

        model = self.unigram(self.train_dataset.get_textColor())
        model1 = self.unigram(self.ref_dataset.get_textColor())
        model2 = self.unigram(self.test_dataset.get_textColor())

        for i in self.train_dataset.get_textColor():
            if (self.perplexity(i, model) < 100):
                counter = counter + 1
                perp = perp + self.perplexity(i, model)
        for i in self.ref_dataset.get_textColor():
            if (self.perplexity(i, model1) < 100):
                counter = counter + 1
                perp = perp + self.perplexity(i, model1)
        for i in self.test_dataset.get_textColor():
            if (self.perplexity(i, model2) < 100):
                counter = counter + 1
                perp = perp + self.perplexity(i, model2)


        print(colored("==begining data (final perplexity)==", 'magenta'))
        print(colored('====> Final Average Perplexity: {:.4f}'.format(perp/counter),'cyan'))
        print(colored("==ending data (final perplexity)==", 'magenta'))
        print("")

    def unigram(self, tokens):    
        model = collections.defaultdict(lambda: 0.01)
        for f in tokens:
            try:
                model[f] += 1
            except KeyError:
                model [f] = 0
                continue
        N = float(sum(model.values()))
        for word in model:
            model[word] = model[word]/N
        return model
    
    def perplexity(self, testset, model):
        testset = testset.split()
        perplexity = 1
        N = 0
        for word in testset:
            N += 1
            perplexity = perplexity * (1/model[word])
        perplexity = pow(perplexity, 1/float(N)) 
        return perplexity

if __name__ == '__main__':
    run = Engine()