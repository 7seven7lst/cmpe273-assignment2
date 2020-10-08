import requests

def perform_action(action, data, response=None, steps=None):
    if action.startswith("::print"):
        if (data =='http.response.headers.content-type'):
            print(response.headers['content-type'])
        elif (data =='http.response.headers.X-Ratelimit-Limit'):
            print(response.headers['X-Ratelimit-Limit'])
    elif action.startswith("::invoke"):
        step_id = action.split(":")[-1]
        invoke_step(step_id, data, steps)
    else:
        raise ValueError('unrecognized action')

def eval_condition(response, is_error, condition, steps):
    if not is_error and condition.get('if'):
        ifblock = condition.get('if')
        left = ifblock['equal']['left']
        right = ifblock['equal']['right']
        if left != 'http.response.code':
            raise ValueError('Unrecognized left condition')
        
        if left == 'http.response.code' and right == response.status_code:
            thenblock = condition.get('then')
            perform_action(thenblock['action'], thenblock['data'], response, steps)
        else:
            elseblock = condition.get('else')
            perform_action(elseblock['action'], elseblock['data'], response, steps)
    else:
        elseblock = condition.get('else')
        if is_error:
            perform_action(elseblock['action'], elseblock['data'], response, steps)

def parse_step(step):
    step_type = step['type']
    step_method = step['method']
    step_outbound_url = step['outbound_url']
    step_condition = step['condition']
    return step_type, step_method, step_outbound_url, step_condition

def invoke_step(step_id, data, steps):
    step_id = int(step_id)
    step = None
    for i in steps:
        if step_id in i:
            step = i
            break
    step_type, step_method, step_outbound_url, step_condition = parse_step(step)
    
    if step_outbound_url == '::input:data':
        step_outbound_url = data 
    response = None
    is_error = False
    if step_type == 'HTTP_CLIENT':
        try:
            response = requests.request(step_method, step_outbound_url)
            is_error = False
        except:
            is_error = True
    else:
        raise ValueError('unrecognized type')
    eval_condition(response, is_error, step_condition, steps)
