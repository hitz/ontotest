import httplib2 as http
import json
import urllib
import sys

from urlparse import urlparse

class OwlServices():

    def __init__(self):

        self.url = 'http://rest.bioontology.org/bioportal'
        self.api_key = 'ba7ec3b3-ae30-4b1e-a686-3781a7fd4ee8'
        ''' for user 'benhitz' '''
        self.ontologies = {}

    def _prep_resource(self, path, data=''):

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8'
        }
        target = self.url+path

        method = 'GET'
        query = urllib.urlencode(data)
        '''
            POST method not enabled for many Bioontology services
            method = 'POST'
            body =  urllib.urlencode(data)
        '''
        url = bool(query) and target+"?"+query or target
        return http.Http().request(
            url, method=method, headers=headers)

    def _decode(self, json_data):

        try:
            return json.loads(json_data)

        except ValueError:
            print "Could not decode: " + json_data
            return {}

    def get_all_ontologies(self):

        response, content = self._prep_resource(
            '/ontologies?apikey='+self.api_key)

        self.oj = self._decode(content)
        try:
            self.oj.has_key('success')
        except:
            print "Failed to get ontologies from " + self.url

        for o in self.oj['success']['data'][0]['list'][0]['ontologyBean']:
            bioo = BioOntology(o)
            self.ontologies[bioo['ontologyId']] = bioo

    def get_ontology(self, ontology_id):

        response, content = self._prep_resource(
            '/virtual/ontology/'+str(ontology_id)+'?apikey='+self.api_key)

        self.oj = self._decode(content)
        try:
            self.oj.has_key('success')
        except:
            print "Failed to get ontology: " + ontology_id + "from " + self.url

        o = self.oj['success']['data'][0]['ontologyBean']
        try:
            assert(type(o)==dict)
        except:
            print "Ontology get failed: " + str(o)

        bioo = BioOntology(o)
        self.ontologies[bioo['ontologyId']] = bioo

    def get_term(self, term, ontology_id):

        if not term: return None
        matches = self.search_term(term, [ontology_id],True)
        ''' webservices bizzarely returns a single object or [] '''
        if (type(matches) == list and len(matches)>1):
            print "More than one match found for term: " + term
            return None
        elif(type(matches) == list and len(matches)==0):
            print "No matches found for %s in %d." % (term, ontology_id)
            return None

        ontology = {
          'id': ontology_id,
          'label': matches['ontologyDisplayLabel'],
          'version_id': matches['ontologyVersionId']
        }
        return self.lookup_term(matches['conceptIdShort'], ontology)

    def lookup_term(self, term_id, ontology):

        search_params = {
            'apikey': self.api_key,
            'conceptid': term_id
        }
        response, content = self._prep_resource('/virtual/ontology/'+str(ontology['id']),
            search_params)

        search_result = self._decode(content)

        try:
            search_result.has_key('success')

            return Term(
                search_result['success']['data'][0]['classBean'],ontology)

        except KeyError:
            print "Could not get full term for %s in %i" % (term_id, ontology['id'])
            return None

    def get_all_terms(self, ontology):
        pass

    def fetch_terms(self, search_result):
        ''' gets all terms from search result array as Term objects '''
        return [ self.lookup_term(t['conceptIdShort'],
                               { 'id'        : t['ontologyId'],
                                 'version_id': t['ontologyVersionId'],
                                 'label'     : t['ontologyDisplayLabel'] }
                                 ) for t in
                 filter(lambda x: not x['isObsolete'], search_result) ]

    def search_term(self, term, ontologies = [], exact=False):

        search_params = {
            'apikey': self.api_key,
            'query': term
        }
        if ontologies:
            search_params['ontologyids'] = ",".join(
                str(ont) for ont in ontologies)

        if exact:
            search_params['isexactmatch'] = 1

        response, content = self._prep_resource('/search/',search_params)
        self.search_result = self._decode(content)
        try:
            self.search_result.has_key('success')
            ''' returns list of "searchBean" dictionarys '''
            if self.search_result['success']['data'][0]['page']['numResultsTotal'] < 1:
                return []

            return self.search_result[
                'success']['data'][0]['page']['contents'][
                'searchResultList']['searchBean'
            ]

        except KeyError:
            print "Term Search failed"  + str(response)
            return []

class DictStruct(object):
    '''The recursive class for building and representing objects with.'''
    def __init__(self, obj):
        for k, v in obj.iteritems():
            if isinstance(v, dict):
                setattr(self, k, DictStruct(v))
            else:
                setattr(self, k, v)

    def __getitem__(self, val):
        return self.__dict__[val]

    def __repr__(self):
        return '{%s}' % str(', '.join('%s : %s' % (k, repr(v)) for
            (k, v) in self.__dict__.iteritems()))


class BioOntology(DictStruct):
    pass

class Term(DictStruct):
    ''' inversion of data structure returned from bioontologies'''

    def __init__(self, obj, ontology):
        super(Term,self).__init__(obj)
        self.SubClass = []
        self.SuperClass = []
        self.definitions = []
        self.ontology = ontology

        # now deal with the relations mess

        for section in self.relations[0]['entry']:
            if len(section) == 2:
                try:
                    for coded_key,coded_value in section.iteritems():
                        if coded_key == 'string':
                            k = coded_value
                            k = k.replace(':','_')
                            #efo:, rdf: screws up object accessors
                        else:
                            v = coded_value
                            val_type = coded_key # could be int, list

                    if k == 'SuperClass' or k == 'SubClass':
                        if bool(v[0]) and type(v[0]['classBean']) == list:
                            try:
                                v = [ { x['id']: x['label'] } for x in v[0]['classBean'] ]
                            except TypeError:
                                print v
                        elif bool(v[0]) and type(v[0]['classBean'] == dict):
                            v = [ {v[0]['classBean']['id']: v[0]['classBean']['label']} ]
                        else:
                            v = []

                    setattr(self,k,v)
                except ValueError:
                    print( "section has too many values: %d (%s)"
                          % section, len(section) )

            else:
                print "ERROR: invalid section %s" % section

        #del self.relations
        # definitions also have odd "string" notation
        setattr(self,'definitions',[ d['string'] for d in self.definitions ])

    def children(self):
        return self.SubClass

    def ancestors(self):
        return self.SuperClass


