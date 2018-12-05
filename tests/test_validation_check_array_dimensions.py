from __future__ import absolute_import
from __future__ import unicode_literals

from os.path import dirname, exists
from shutil import rmtree
import os.path
from pytest import raises


def test_validation_check_array_dimensions():
    """
    checks that arrays with more than 1 dimension name the indicies.
    """

    import itemlang.codegen as codegen

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
                    model_string="""
                    // model
                    package types {
                        type int as custom {}
                        type UINT16 as custom {}
                        type float as custom {}
                    }
                    package mypackage1 {
                    target_namespace "mypackage1.test"
                        struct Simple {
                            scalar n        : types.UINT16 {default="5"}
                            array  a_ui16   : types.UINT16[n:x][2*n:y]
                        }
                    }
                    """)

    # ---------------------------
    # error 1
    # ---------------------------
    with raises(Exception, match=r'array .* needs to have named ' +
                                 'dimensions: specify .*'):
        codegen.codegen(srcgen_folder=dest_folder,
                        model_string="""
    // model
    package types {
        type int as custom {}
        type UINT16 as custom {}
        type float as custom {}
    }
    package mypackage1 {
        target_namespace "mypackage1.test"
        struct Simple {
            scalar n        : types.UINT16 {default="5"}
            array  a_ui16   : types.UINT16[n][2*n:y] // missing dimension name
        }
    }
                        """)

    # ---------------------------
    # error 1
    # ---------------------------
    with raises(Exception, match=r'array .* needs to have named ' +
                                 'dimensions: specify .*'):
        codegen.codegen(srcgen_folder=dest_folder,
                        model_string="""
    // model
    package types {
        type int as custom {}
        type UINT16 as custom {}
        type float as custom {}
    }
    package mypackage1 {
    target_namespace "mypackage1.test"
        struct Simple {
            scalar n        : types.UINT16 {default="5"}
            array  a_ui16   : types.UINT16[n][2*n] // missing dimension name
        }
    }
                        """)

    #################################
    # END
    #################################

    # nothing generated: rmtree(dest_folder)
    assert not exists(dest_folder)
