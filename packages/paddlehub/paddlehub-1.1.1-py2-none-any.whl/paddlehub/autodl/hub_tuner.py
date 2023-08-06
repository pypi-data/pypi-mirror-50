# -*- coding: utf-8 -*-

from evaluator import AutoDeepLearningEvaluator
from autodl import AutoDeepLearning


if __name__=="__main__":
    
    eva = AutoDeepLearningEvaluator("evaluate.ini")
    
    eva.set_task_name(task_name='text-cls')
    
    algo = AutoDeepLearning("algorithm.json")
    
    algo.init(eva)
    
    run_round_count = 0
    max_run_round = 1
    while (not algo.is_stop() and run_round_count < max_run_round):
        algo.step(is_debug=False)
        run_round_count = run_round_count + 1

    print("optimal_solution")
    print(eva.convert_params(algo.optimal_solution()))
    print('success')