def best_scores(model, metric):
    res = model.evals_result()
    best = model.best_iteration
    return (res["validation_1"][metric][best], res["validation_0"][metric][best])

def clear_gpu(model):
    try:
        model.get_booster().__del__()
    except: 
            pass
    