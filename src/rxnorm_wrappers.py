## -------------------------------------------
## package  : cdwrx
## author   : evan.phelps@gmail.com
## created  : Tue Mar 20 18:04:28 EST 2016
## vim      : ts=4


from cdwlib.throttle import throttle
import requests


@throttle(per_sec=20)
def rxnorm_req(resource, **kwargs):
    is_json = True
    if 'rxnorm_base' not in kwargs:
         kwargs['rxnorm_base'] = 'https://rxnav.nlm.nih.gov/REST/'
    if 'json' in kwargs:
        is_json = kwargs['json']
    if is_json:
        resource += '.json'
    
    attrs = ['%s=%s'%(attr,val) for (attr,val) in
             kwargs.items() if attr != 'rxnorm_base']
    
    req = kwargs['rxnorm_base'] + resource + '?%s'%('&'.join(attrs))
    
    resp = requests.get(req)
    
    return resp.json() if is_json else resp


def coerce_rxcui(rxcui):
    json = rxnorm_req('rxcui/%s/status'%rxcui)
    status = json['rxcuiStatus']['status']
    
    if status in ('Retired', 'Unknown', 'Alien'):
        warning('Cannot coerce! status = %s'%status)
        return None
    
    retval = json['rxcuiStatus']['minConceptGroup']['minConcept'][0]['rxcui']
    return retval


def get_status(rxcui):
    json = rxnorm_req('rxcui/%s/status'%rxcui)
    status = json['rxcuiStatus']['status']
    return status


def get_TTY(rxcui):
    json = rxnorm_req('rxcui/%s/property'%rxcui, propName='TTY')
    return json['propConceptGroup']['propConcept'][0]['propValue']


def get_props(rxcui, skip_coerce=False):
    json = rxnorm_req('rxcui/%s/properties'%rxcui)
    key = 'properties'
    props = None
    if json is None:
        if skip_coerce == False:
            rxcui_new = coerce_rxcui(rxcui)
            if rxcui_new is not None:
                props = get_props(coerce_rxcui(rxcui),
                                  skip_coerce=True)
    else:
        props = json[key]
    
    return props


def get_ins(rxcui):
    json = rxnorm_req('rxcui/%s/related'%rxcui, tty='IN')
    try:
        retval = [(y['rxcui'], y['name']) for y in
                  [x['conceptProperties'] for x in
                   json['relatedGroup']['conceptGroup']][0]]
    except KeyError, e:
        warning('missing key %s'%e)
        return []
    return retval

