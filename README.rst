====================================
Custom interface definition language
====================================

.. image:: https://travis-ci.org/goto40/itemlang.svg?branch=master
    :target: https://travis-ci.org/goto40/itemlang

This is an example of custom interface definition language. It mainly targets C++.

Rough outline
====================================

Requirements
-------------

1. Items are composed of scalar and array attributes.
2. An attribute type is either a raw type (like an integer) or an item type.
3. A raw type can be mapped to language specific types (e.g., C++ types).
4. Array attributes can have one or more dimensions.
5. Array dimensions are either fixed or depend on other scalar attributes.
6. Array sizes and scalar attributes used to determine their size must be synchronized at all times (invariant).
7. Meta information, such as min/max values, must be provided for each attribute.
8. Iteration over attributes must be supported in a generic way, in order to support textual and binary serialization.


Generated C++ Code
--------------------------

1. Attributes are represented as public instances of an attribute wrapper.
 * This wrapper contain the data itself and implicit conversions to make its usage as simple as possible: 
   the goal is to make data access feel like a POD attribute access.
 * The wrapper declares its container as friend to grant its owner potentially more access rights than 
   during an external access.
2. Scalar attributes utilized to determine array sizes must be protected from uncontrolled modification.
 * a special read only attribute wrapper represents such attribute.
 * An init function is provided to allow to set scalar attributes utilized to determine array sizes.
3. Array sizes support formulas with integers, scalar attributes of the current item or scalar attributes 
   of items included as scalar attributes of the current item (depth 3, e.g., header.part1.n).
4. Meta information about attributes and structures are provided as compile time information (template
   arguments and/or constexpr expressions and functions)


Installation
--------------------------

See file ".travis.yml"


Use the code generator
--------------------------

Get help:
::
        $ itemc --help


Run code generation for C++:
::
        $ itemc example.myidl --generate-cpp


Current state
-------------------
 * General:
  * Check syntax of default values (later also min/max), differentiate between float/signed/unsigned)
  * Check constant fields (not included)
  * Check bitfields (not included)
 * C++: working
 * Python: no so well tested, working ... (also check Python 3.7 data classes)
 * Octave:
  * no checks (add check consistency function; automatically call after read, before write)
  * no tests (just a demo; do we have unittests like in matlab?)
 * Python-construct: not integrated