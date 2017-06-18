from rdflib import *
from rdflib.namespace import RDF, FOAF, RDFS
import sys


class OntologyEdit:

    def __init__(self):
        self.g = Graph()

    def openOntology(self, filename):
        self.g.parse(filename, format="turtle")

    def viewOntology(self):
        print(self.g.serialize(format='turtle'))

    def createOntology(self, supertopic, supertopicURI):
        self.g.add((supertopicURI, RDF.type, FOAF.Topic))
        self.g.add((supertopicURI, FOAF.name, Literal(supertopic)))
        self.viewOntology()

    def addSubtopic(self, subtopic, subtopicURI, supertopic, supertopicURI):
        self.g.add((subtopicURI, RDFS.subClassOf, supertopicURI))
        #self.g.add((subtopicURI, RDF.type, FOAF.Topic))
        self.g.add((subtopicURI, FOAF.name, Literal(subtopic)))

    def removeSubtopic(self, subtopicURI):
        for s, p, o in self.g.triples((None, RDFS.subClassOf, None)):
            if o == subtopicURI:  # if subtopic is supertopic
                self.removeSubtopic(s)
                self.g.remove((s, None, None))
        self.g.remove((subtopicURI, None, None))

    def saveOntology(self, filename):
        self.g.serialize(destination=filename, format='nt')


ontologyEdit = OntologyEdit()
# n = Namespace("http://example.org/people/")

answer = True

while answer:
    print("""
    1. Open ontology
    2. Create ontology
    3. View ontology
    4. Add subtopic
    5. Remove subtopic
    6. Save ontology
    7. Exit
    """)

    answer = raw_input("What would you like?\n" )
    if answer == "1":
        print("\n Will open ontology")
        filename = raw_input("Enter file name: ")
        ontologyEdit.openOntology(filename)

    elif answer == "2":
        supertopic = raw_input("Enter supertopic to add: ")
        supertopicURI = Literal(supertopic)
        print(supertopic, supertopicURI)
        ontologyEdit.createOntology(supertopic, supertopicURI)

    elif answer == "3":
        ontologyEdit.viewOntology()

    elif answer == "4":
        subtopic = raw_input("Enter subtopic to add: ")
        subtopicURI = Literal(subtopic)
        supertopic = raw_input("Enter supertopic: ")
        supertopicURI = Literal(supertopic)
        ontologyEdit.addSubtopic(subtopic, subtopicURI, supertopic, supertopicURI)

    elif answer == "5":
        subtopic = raw_input("Enter subtopic to remove: ")
        subtopicURI = Literal(subtopic)
        ontologyEdit.removeSubtopic(subtopicURI)

    elif answer == "6":
        filename = raw_input("Enter file name: ")
        ontologyEdit.saveOntology(filename)

    elif answer == "7":
        print("\n Goodbye!")
        answer = False

    elif answer != "":
        print("\n Incorrect input. Try again.")



