# -*- coding: utf-8 -*-
from multiprocessing.pool import ThreadPool
import io
import os
import copy
import sys
import numpy
import cma
import json


class AutoDeepLearning():
    def __init__(self, evaluator, thread=1, popsize=1, sigma=0.2):
#         with io.open(config_path, 'r', encoding='utf8') as f:
#             self.config = json.load(f)['algorithms'][0]
        self._thread = thread #self.config['thread']
        self._popsize = popsize #self.config['popsize']
        self._sigma = sigma #self.config['sigma']
        
        self.evaluator = evaluator
        init_input = evaluator.get_init_params()
        print(init_input)
        self.evolution_stratefy = cma.CMAEvolutionStrategy(init_input, 
                                                           sigma, 
                                                           {'popsize':self.popsize, 
                                                            'bounds':[-1, 1], 
                                                            'AdaptSigma':True, 
                                                            'verb_disp':1,
                                                            'verb_time':'True',})

    @property
    def thread(self):
        return self._thread

    @property
    def popsize(self):
        return self._popsize
    
    @property
    def sigma(self):
        return self._sigma
        
    def is_stop(self):
        return self.evolution_stratefy.stop()

    def solutions(self):
        return self.evolution_stratefy.ask()

    def feedback(self, params_list, reward_list):
        self.evolution_stratefy.tell(params_list, reward_list)
        self.evolution_stratefy.logger.add()
        self.evolution_stratefy.disp()

    def optimal_solution(self):
        return list(self.evolution_stratefy.result.xbest)
    
    def multi_run_wrapper(args):
        return self.evaluator.run(*args)

    def step(self):
#         if self.is_stop():
#             return 1
        solutions = self.solutions()
        
        params_cudas = []
        for idx in range(len(solutions)):
            solution = solutions[idx]
            num_cuda = idx
            params_cudas.append([solution, num_cuda])
        
        tp = ThreadPool(self.thread)

        
        solution_results = tp.map(self.evaluator.run, params_cudas)
        tp.close()
        tp.join()

        self.feedback(solutions, solution_results)
        return 0
    
        
    
    