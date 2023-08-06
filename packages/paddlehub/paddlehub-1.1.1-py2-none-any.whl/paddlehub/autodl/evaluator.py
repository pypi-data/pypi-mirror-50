# -*- coding: utf-8 -*-

import io
import json
import os
import random


class AutoDeepLearningEvaluator():
    def __init__(self, params_file):
        with io.open(params_file, 'r', encoding='utf8') as f:
            self.params = json.load(f)
        
        self.run_cmd = "python -u finetunee-cola.py" #self.config['autodl']['run_cmd']
        
    def set_task_name(self, task_name):
        self.task_name = task_name 
    
    def get_init_params(self):
        init_params = []
        for param in self.params["param_list"]:
            init_params.append(param['init_value'])
        init_params = self.inverse_convert_params(init_params)
        return init_params
       
    def get_reward(self, result_output):
        return 100 - float(result_output)

    def is_valid_params(self, params):
        for i in range(0, len(self.params["param_list"])) :
            if params[i] < float(self.params["param_list"][i]["greater_than"]):
                return False
            if params[i] > float(self.params["param_list"][i]["lower_than"]):
                return False
        return True

    def convert_params(self, params):
        cparams = []
        for i in range(0,len(self.params["param_list"])) :
            cparams.append(float(self.params["param_list"][i]["greater_than"]+(params[i]+1.0)/2.0*(
                    self.params["param_list"][i]["lower_than"]-self.params["param_list"][i]["greater_than"])))
            if cparams[i] <= float(self.params["param_list"][i]["greater_than"]):
                cparams[i] = float(self.params["param_list"][i]["greater_than"])
            if cparams[i] >= float(self.params["param_list"][i]["lower_than"]):
                cparams[i] = float(self.params["param_list"][i]["lower_than"])
            if self.params["param_list"][i]["type"] == "int":
                cparams[i] = int(cparams[i])
            print(self.params["param_list"][i]["name"]+"\t"+str(cparams[i]))
        return cparams

    def inverse_convert_params(self, params):
        cparams = []
        for i in range(0,len(self.params["param_list"])):
            cparams.append(float(-1.0+2.0*(params[i]-self.params["param_list"][i]["greater_than"])/(
                    self.params["param_list"][i]["lower_than"]-self.params["param_list"][i]["greater_than"])))
            if cparams[i] <= -1.0:
                cparams[i] = -1.0
            if cparams[i] >= 1.0:
                cparams[i] = 1.0
        return cparams

    def format_params_str(self, params):
        param_str="--%s=%s" % (self.params["param_list"][0]["name"], params[0])
        for i in range(1, len(self.params["param_list"])) :
            param_str = "%s --%s=%s" % (param_str, self.params["param_list"][i]["name"], str(params[i]))
        return param_str
        
    def run(self, *args):
        params = args[0][0]
        num_cuda = args[0][1]
        params = self.convert_params(params)
        if not self.is_valid_params(params):
            return 100
        # 超参数对应值, 如
        # --learning_rate=5.78071736959e-05 --weight_decay=0.00680632823548 --batch_size=32 --warmup_prop=0.114844887289
        param_str = self.format_params_str(params)
        run_name = self.task_name+"-r"+str(random.randint(0,10000))+"-"+str(random.randint(0,10000))
        ckpt_dir = self.task_name+"-ckpt-"+param_str.replace(" ", "")+"-"+str(random.randint(0,10000))
        logfile = run_name+param_str.replace(" ", "")+".log"
        run_cmd = "export CUDA_VISIBLE_DEVICES=%s; %s --save=%s --acc_log=%s --checkpoint_dir=%s %s" % (
            num_cuda, self.run_cmd, run_name, logfile, ckpt_dir, param_str)
        try:
            os.system(run_cmd)
            with io.open(logfile, 'r', encoding='utf8') as f:
                val = f.read().split(" ")[0]
            # val = open(logfile).read().split(' ')[0]
        except:
            val = 0.0
        return self.get_reward(val)       
        
        
        
        
        