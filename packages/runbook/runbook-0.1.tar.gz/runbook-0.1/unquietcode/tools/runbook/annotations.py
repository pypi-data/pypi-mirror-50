

def step(name=None, repeatable=None, skippable=None, critical=None):
    """
    name => provide a custom name instead of using the method name
    repeatable => allow the step to repeat even if it has already been completed
    skippable => allow the step to be skipped even it has yet to be completed
    critical => whether it is possible to continue after this step if it fails or is skipped
    
    timeout? - how long to wait before giving up (then continuing or failing)
    """

    # these should be handled in the lower level code
    # repeatable = False if repeatable is None else repeatable
    # skippable = False if skippable is None else skippable
    # critical = False if critical is None else critical
    # 
    def decorator(fn):
        fn.__annotations__['UQC_RUNBOOK_NAME'] = name
        fn.__annotations__['UQC_RUNBOOK_REPEAT'] = repeatable
        fn.__annotations__['UQC_RUNBOOK_SKIP'] = skippable
        fn.__annotations__['UQC_RUNBOOK_CRITICAL'] = critical
        
        return fn
    
    return decorator


@step(name="custom step name", repeatable=True)
def some_step():
    pass
    
    

# alternative style

    
def some_step(name="custom step name", repeatable=True, skippable=False):
    pass