import unittest

class TestOWLservice(unittest.TestCase):

    def setUp(self):
        import OWLServices
        self.service = OWLServices.OwlServices()

    def test_get_all_ontogies(self):
        s = self.service
        s.get_all_ontologies()

        self.assertGreater(len(s.ontologies.keys()), 2 ,
                      "Number of ontologies: "+str(len(s.ontologies.keys())))

    def test_has_efo(self):
        s = self.service
        s.get_all_ontologies()
        efo_id = 1136
        self.assertIs(s.ontologies.has_key(efo_id), True,
                      "EFO not found: "+str(efo_id))

    def test_get_efo(self):
        s = self.service
        efo_id = 1136
        s.get_ontology(efo_id)
        ontology = s.ontologies[efo_id]
        self.assertEquals(ontology['displayLabel'],
            "Experimental Factor Ontology", "EFO has wrong name: " +
            ontology['displayLabel'])

    def test_search(self):

        s = self.service
        term = 'ChIP-Seq'
        result = s.search_term(term)
        self.assertGreater(len(result),20, "Search for "+term+
            " has <= 20 results: "+str(len(result)))

        self.assertGreater(filter(bool, [
            bool(ele['conceptIdShort'].find('EFO')>0) and
                ele['conceptIdShort'] for ele in result ]), 1,
        "No EFO like terms found")

    def test_search_exact(self):

        s = self.service
        term = 'ChIP-Seq'
        result = s.search_term(term, [],True)
        print result
        self.assertEquals(len(result),5, "Exact search for "+term+
            " has <> 5 results: "+str(len(result)))

        self.assertGreater(filter(bool, [
            bool(ele['conceptIdShort'].find('EFO')>0) and
                ele['conceptIdShort'] for ele in result ]), 1,
        "No EFO like terms found (exact)")

    def test_bad_lookup(self):
        s = self.service
        term = 'ChIP-Seq'
        bad_id = 99109934848890292
        term = s.get_term(term,bad_id)
        self.assertIs(term, None,
         "Should have returned nothing for bad ontology id")

    def test_missing_term(self):
        s = self.service
        term = "thisanintinnoontologyd000d!!#!#"
        result = s.search_term(term)
        self.assertEqual(result,[],
         "Should have returned nothing for bad term")

    def test_lookup_term_efo(self):
        s = self.service
        term_name = 'ChIP-Seq'
        efo_id = 1136
        term = s.get_term(term_name,efo_id)
        self.assertNotEqual(term, None, "No EFO term found: "+ str(term))
        self.assertEqual(term['id'],'efo:EFO_0002692',
            "Correct EFO id EFO_0002692 not found: " + term['id'])

    def test_fetch_terms(self):
        s = self.service
        term_name = 'monocyte'
        search = s.search_term(term_name,[],True)
        self.assertGreater(len(search),24, "Fewer than 25 monocyte hits found")

        s.fetch_terms(search)

    def test_show_children(self):
        ''' Note: Children in OWL are SubClasses '''
        s = self.service
        term_name = 'ChIP-Seq'
        efo_id = 1136
        term = s.get_term(term_name, efo_id)
        self.assertEqual(term.children(), [],
         "ChIP has children %s" % term.children())
        term_name = 'monocyte'

        known_children  = [
          [],
          [{u'X80VL': u'Monoblast'}, {u'X80VK': u'Promonocyte'}],
          [],
          [],
          [],
          [{u'http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#Immature_Monocyte': u'Immature Monocyte'}],
          [{u'CL:CL_0000860': u'CL:CL_0000860'},
           {u'CL:CL_0002393': u'CL:CL_0002393'},
           {u'CL:CL_0001022': u'CL:CL_0001022'},
           {u'CL:CL_0000875': u'CL:CL_0000875'}],
          [{u'http://ihtsdo.org/snomedct/anatomy#41621006': u'Myelomonocyte'},
           {u'http://ihtsdo.org/snomedct/anatomy#58986001': u'Macrophage'},
           {u'http://ihtsdo.org/snomedct/anatomy#1075005': u'Promonocyte'}],
          [],
          [{u'CL:CL_0000860': u'inflammatory monocyte'},
           {u'CL:CL_0002393': u'intermediate monocyte'},
           {u'CL:CL_0001022': u'CD115-positive monocyte'},
           {u'CL:CL_0000875': u'patrolling monocyte'}],
          [{u'BTO:0004657': u'premonocyte'}, {u'BTO:0000801': u'macrophage'}],
          [{u'EV:0200181': u'splenocyte'}],
          [{u'CL:0000875': u'resident monocyte'},
           {u'CL:0000860': u'inflammatory monocyte'},
           {u'CL:0000235': u'macrophage'},
           {u'CL:0000092': u'osteoclast'},
           {u'CL:0000782': u'myeloid dendritic cell'},
           {u'CL:0000840': u'immature myeloid dendritic cell'}],
          [{u'FMA:63841': u'Plasma membrane'}, {u'FMA:67261': u'Protoplasm'}],
          [{u'CL:0000235': u'macrophage'},
           {u'CL:0000092': u'osteoclast'},
           {u'CL:0000782': u'myeloid dendritic cell'},
           {u'CL:0000860': u'classical monocyte'},
           {u'CL:0002393': u'intermediate monocyte'},
           {u'CL:0000875': u'non-classical monocyte'},
           {u'CL:0001022': u'CD115-positive monocyte'}],
          [{u'CL:0000235': u'macrophage'},
           {u'CL:0000092': u'osteoclast'},
           {u'CL:0000782': u'myeloid dendritic cell'},
           {u'CL:0000860': u'inflammatory monocyte'},
           {u'CL:0002393': u'intermediate monocyte'},
           {u'CL:0001022': u'CD115-positive monocyte'},
           {u'CL:0000875': u'patrolling monocyte'}],
          [{u'Immature_Monocyte': u'Immature Monocyte'}],
          [{u'http://purl.org/obo/owl/CL#CL_0000860': u'classical monocyte'},
           {u'http://purl.org/obo/owl/CL#CL_0002393': u'intermediate monocyte'},
           {u'http://purl.org/obo/owl/CL#CL_0001022': u'CD115-positive monocyte'},
           {u'http://purl.org/obo/owl/CL#CL_0000875': u'non-classical monocyte'}],
          [{41621006: u'Myelomonocyte'},
           {58986001: u'Macrophage'},
           {1075005: u'Promonocyte'}],
          [{u'TAO:0009047': u'osteoclast'}, {u'TAO:0009141': u'macrophage'}],
          [{u'ZFA:0009047': u'osteoclast'}, {u'ZFA:0009141': u'macrophage'}],
          [{u'CL:CL_0000860': u'classical monocyte'},
           {u'CL:CL_0002393': u'intermediate monocyte'},
           {u'CL:CL_0001022': u'CD115-positive monocyte'},
           {u'CL:CL_0000875': u'non-classical monocyte'}],
          [],
          None,
          [{u'Leukocyte_Monocyte_Macrophage_MMHCC': u'Mouse Macrophage'}]
        ]

        search = s.search_term('monocyte',[],True)
        terms = s.fetch_terms(search)
        self.assertItemsEqual( terms.children(), known_children,
            "Monocyte ancestors are different %s" % terms.ancestors() )

    def test_show_ancestors(self):
        ''' Note: Ancestors in OWL are SuperClasses '''
        s = self.service
        term_name = 'ChIP-Seq'
        super_classes = [
        [u'efo:EFO_0002697'], [u'efo:EFO_0004120'], [u'efo:EFO_0001456']
        ]
        efo_id = 1136
        term = s.get_term(term_name, efo_id)
        self.assertEqual(len(term.ancestors()), 3,
         "ChIP-Seq has incorrect number of ancestors %s" % term.ancestors())
        self.assertEqual([x.keys() for x in term.ancestors()],
                         super_classes, "ChIP-Seq has wrong ancestors")
        term_name = 'monocyte'
        known_parents = [
         [{u'0435-4175': u'leukocyte'}],
         [{u'X80Uw': u'White blood cell'}],
         [{u'FMA:FMA_62855': u'Nongranular leukocyte'}],
         [{u'fma:Nongranular_leukocyte': u'Nongranular leukocyte'}],
         [{u'GranulocyteOrMonocyte': u'GranulocyteOrMonocyte'}],
         [{u'http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#Leukocyte': u'Leukocyte'}],
         [{u'efo:EFO_0000324': u'efo:EFO_0000324'},
          {u'CL:CL_0000766': u'CL:CL_0000766'}],
         [{u'http://ihtsdo.org/snomedct/anatomy#404798000': u'Peripheral blood mononuclear cell'}],
         [{u'FMA:62855': u'Nongranular leukocyte'}],
         [{u'CL:CL_0002087': u'nongranular leukocyte'},
          {u'CL:CL_0000766': u'myeloid leukocyte'}],
         [{u'BTO:0001433': u'mononuclear phagocyte'}, {u'BTO:0000751': u'leukocyte'}],
         [{u'EV:0200000': u'Cell Type'}],
         [{u'CL:0000766': u'myeloid leukocyte'}, {u'CL:0000559': u'promonocyte'}],
         [{u'FMA:62855': u'Nongranular leukocyte'}],
         [{u'CL:0000559': u'promonocyte'},
          {u'CL:0002087': u'nongranular leukocyte'},
          {u'CL:0000766': u'myeloid leukocyte'}],
         [{u'CL:0000559': u'promonocyte'},
          {u'CL:0002087': u'nongranular leukocyte'},
          {u'CL:0000766': u'myeloid leukocyte'}],
         [{u'Leukocyte': u'Leukocyte'}],
         [{u'efo:EFO_0000324': u'cell type'},
          {u'http://purl.org/obo/owl/CL#CL_0000766': u'myeloid leukocyte'}],
         [{404798000: u'Peripheral blood mononuclear cell'}],
         [{u'TAO:0009253': u'promonocyte'},
          {u'TAO:0009064': u'mononuclear phagocyte'},
          {u'TAO:0009088': u'professional antigen presenting cell'}],
         [{u'ZFA:0009253': u'promonocyte'},
          {u'ZFA:0009064': u'mononuclear phagocyte'},
          {u'ZFA:0009088': u'professional antigen presenting cell'}],
         [{u'CL:CL_0000766': u'myeloid leukocyte'}],
         [],
         None,
         [{u'Leukocyte_WBC_MMHCC': u'Mouse Leukocyte'}]
        ]

        search = s.search_term('monocyte',[],True)
        terms = s.fetch_terms(search)
        self.assertEquals(len(terms),25,
            "Monocyte search returned %d terms" % len(terms))

        self.assertItemsEqual( terms.ancestors(), known_parents,
            "Monocyte ancestors are different %s" % terms.ancestors() )


