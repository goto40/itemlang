from __future__ import absolute_import
from __future__ import unicode_literals

from os.path import dirname, exists
from shutil import rmtree
import os.path
from pytest import raises


def test_validation_CheckRawTypes():
    """
    checks that addon info for used types for specific languages are defined.
    """

    import itemlang.itemc.codegen as codegen

    #################################
    # Model definition and Code creation
    #################################

    this_folder = dirname(__file__)
    dest_folder = os.path.join(this_folder, "src-gen")
    # cleanup old generated code
    if exists(dest_folder):
        rmtree(dest_folder)

    # ---------------------------
    # no error
    # ---------------------------
    codegen.codegen(srcgen_folder=dest_folder,
                    generate_cpp=True,
                    model_string=
                    """
                    // model
                    package types {
                        type int as custom { C++: "int"}
                        type UINT16 as custom {}
                        type float as custom {}
                    }
                    package mypackage1 {
                    target_namespace "mypackage1.test"
                        struct Simple {
                            scalar x        : types.int
                        }
                    }
                    """)

    # ---------------------------
    # error 1
    # ---------------------------
    with raises(Exception, match=r'C\+\+ type is required to generate C\+\+ code for float'):
        codegen.codegen(srcgen_folder=dest_folder,
                        generate_cpp=True,
                        model_string=
                        """
                        // model
                        package types {
                            type int as custom { C++: "int"}
                            type UINT16 as custom {}
                            type float as custom {}
                        }
                        package mypackage1 {
                        target_namespace "mypackage1.test"
                            struct Simple {
                                scalar x        : types.int
                                scalar y        : types.float
                            }
                        }
                        """)

    #################################
    # END
    #################################

    rmtree(dest_folder)
    assert not exists(dest_folder)
