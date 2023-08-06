# pyTBSHACL
Python wrapper for TopBraid's SHACL validator.

[PySHACL](https://github.com/RDFLib/pySHACL) for RDFLib 
[does not currently implement](https://github.com/RDFLib/pySHACL/blob/master/FEATURES.md) 
some of the [advanced SHACL functionality](https://www.w3.org/TR/shacl-af/) 
which is available with [TopBraid's command line validator](https://github.com/TopQuadrant/shacl). 
`pyTBSHACL` implements a python wrapper for the TopBraid validator tool 
to help simplify integration with python projects 
needing that functionality. It is anticipated that this module will 
become redundant as adavanced capabilities are progeressively added to PySHACL.

## Status

Currently (2019-08-12) an initial draft implementation, tested on OS X only.


## Installation

1. Download and install the TopBraid SHACL validator, following guidance at:

  https://github.com/TopQuadrant/shacl
  
2. Set the `SHACLROOT` environment variable to the absolute path to the
`bin` folder of the TopBraid SHACL validator distribution.

3. Clone this repo, cd to the folder, then run: `pip install -e .`

## Example

Following are run from the `examples` folder.

Valid data:

```
$ shacl -d data_00a.ttl -s shape_00.ttl
SLF4J: Failed to load class "org.slf4j.impl.StaticLoggerBinder".
SLF4J: Defaulting to no-operation (NOP) logger implementation
SLF4J: See http://www.slf4j.org/codes.html#StaticLoggerBinder for further details.
@prefix ex:    <http://example.org/> .
@prefix sh:    <http://www.w3.org/ns/shacl#> .
@prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix owl:   <http://www.w3.org/2002/07/owl#> .
@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .

[ a            sh:ValidationReport ;
  sh:conforms  true
] .
===
CONFORMS = True
```

Invalid data:

```
$ shacl -d data_00b.ttl -s shape_00.ttl
SLF4J: Failed to load class "org.slf4j.impl.StaticLoggerBinder".
SLF4J: Defaulting to no-operation (NOP) logger implementation
SLF4J: See http://www.slf4j.org/codes.html#StaticLoggerBinder for further details.
@prefix ex:    <http://example.org/> .
@prefix sh:    <http://www.w3.org/ns/shacl#> .
@prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix owl:   <http://www.w3.org/2002/07/owl#> .
@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .

[ a            sh:ValidationReport ;
  sh:conforms  false ;
  sh:result    [ a                             sh:ValidationResult ;
                 sh:focusNode                  ex:bob ;
                 sh:resultMessage              "Missing expected value ex:Mathematics" ;
                 sh:resultPath                 ex:field ;
                 sh:resultSeverity             sh:Violation ;
                 sh:sourceConstraintComponent  sh:HasValueConstraintComponent ;
                 sh:sourceShape                []
               ]
] .
===
CONFORMS = False
```

Valid Dataset with encoding in json-ld:

```
$ shacl -d data_01a.json -df json-ld  -s shape_01.ttl
SLF4J: Failed to load class "org.slf4j.impl.StaticLoggerBinder".
SLF4J: Defaulting to no-operation (NOP) logger implementation
SLF4J: See http://www.slf4j.org/codes.html#StaticLoggerBinder for further details.
@prefix :      <http://schema.org/> .
@prefix sh:    <http://www.w3.org/ns/shacl#> .
@prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix owl:   <http://www.w3.org/2002/07/owl#> .
@prefix xml:   <http://www.w3.org/XML/1998/namespace> .
@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .

[ a            sh:ValidationReport ;
  sh:conforms  true
] .
===
CONFORMS = True
```

Invalid Dataset encoding:

```
$ shacl -d data_01b.ttl -s shape_01.ttl
SLF4J: Failed to load class "org.slf4j.impl.StaticLoggerBinder".
SLF4J: Defaulting to no-operation (NOP) logger implementation
SLF4J: See http://www.slf4j.org/codes.html#StaticLoggerBinder for further details.
@prefix schema: <http://schema.org/> .
@prefix ex:    <http://example.org/> .
@prefix sh:    <http://www.w3.org/ns/shacl#> .
@prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix owl:   <http://www.w3.org/2002/07/owl#> .
@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .

[ a            sh:ValidationReport ;
  sh:conforms  false ;
  sh:result    [ a                             sh:ValidationResult ;
                 sh:focusNode                  ex:dataset2_encoding ;
                 sh:resultMessage              "schema:contentUrl is required for the encoding property of a Dataset" ;
                 sh:resultPath                 schema:contentUrl ;
                 sh:resultSeverity             sh:Violation ;
                 sh:sourceConstraintComponent  sh:MinCountConstraintComponent ;
                 sh:sourceShape                []
               ]
] .
===
CONFORMS = False
```