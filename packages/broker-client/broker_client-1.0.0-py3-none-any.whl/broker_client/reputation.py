
"""
This code is useful for reputation. However it is out-of-date. Can be used as reference in the future.

reputations_dict = {}

def authorize_request(request,
                      put_owner_feedback=False,
                      broker_url="http://localhost:4000/broker",
                      use_reputation_handler=True):
    headers_dict = dict(request.headers['x-m2m-origin'])
    r = requests.post(broker_url+"/authorization-requests", json=headers_dict)
    if use_reputation_handler:
        msg = request_watcher_for_providers(r, headers_dict['consumer_id'], put_owner_feedback)
    else:
        msg = None
    return {'validation':(r.status_code == 200),'reputations_dict':reputations_dict,'msg':msg}

def request_watcher_for_providers(request, consumer_id, put_owner_feedback=False):
    global reputations_dict
    end_time = request.headers['expiration-time']   # Vai vir do request
    validation = (request.status_code == 200)
    if (not consumer_id in reputations_dict or reputations_dict['trades'] >= 1) and end_time:
        if not consumer_id in reputations_dict:
            reputations_dict[consumer_id] = {'fails':0,'uses':0,'end_time':end_time,'trades':0}
        delay = calculate_seconds_to_expiration(end_time)
        if delay > 0:
            t = Timer(delay+1, send_reputation, (consumer_id, put_owner_feedback))
            t.start()
    elif not end_time:
        reputations_dict[consumer_id]['fails'] += 5
        return "Never heard about you. Please first start negotiation throught Broker"
    if validation:
        reputations_dict[consumer_id]['uses'] += 1
        return "Everything OK with your request"
    else:
        reputations_dict[consumer_id]['fails'] += 1
        return "Permission expired. Negotiate again with me throught Broker to use my resource(s)"

def request_watcher_for_consumers(request, provider_id):
    global reputations_dict
    validation = (request.status_code == 200)
    if not provider_id in reputations_dict:
        reputations_dict[provider_id] = {'fails':0,'uses':0,'trades':0}
    if validation:
        reputations_dict[provider_id]['uses'] += 1
    else:
        reputations_dict[provider_id]['fails'] += 1
    return {'validation':validation,'reputations_dict':reputations_dict,'resource':request.json()}

def calculate_seconds_to_expiration(str_expiration):
    return int(str_expiration) - int(time.time())

def compute_reputation(service_id, put_owner_feedback=False, owner_feedback=None):
    if reputations_dict[service_id]['uses'] >= 1:
        fails = float(reputations_dict[service_id]['fails'])/reputations_dict[service_id]['uses']
    else:
        fails = int(reputations_dict[service_id]['fails'])/2
    if fails > 2.5:
        fails = 2.5
    request_feedback = 5 - fails*2
    if put_owner_feedback:
        if not owner_feedback:
            owner_feedback = int(input("Por favor, insira o seu feedback para o serviço "
                                        + str(service_id) + " num intervalo de 0 a 5: "))
        return (owner_feedback+request_feedback)/2
    else:
        return request_feedback

def send_reputation(service_id, 
                    put_owner_feedback=False, 
                    owner_feedback=None, 
                    broker_url='http://localhost:4000/broker'):
    reputation = compute_reputation(service_id, put_owner_feedback, owner_feedback)
    broker_url = broker_url + '/reputations'
    status = 0
    while status != 200:
        r = requests.post(broker_url, json={'service_id':service_id, 'reputation': reputation})
        status = r.status_code
    reputations_dict[service_id]['fails'] = 0
    reputations_dict[service_id]['uses'] = 0
    reputations_dict[service_id]['trades'] += 1
"""
