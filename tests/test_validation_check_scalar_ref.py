from __future__ import absolute_import
from __future__ import unicode_literals

from os.path import dirname, exists
from shutil import rmtree
import os.path
from pytest import raises


def test_validation_check_scalar_ref():
    """
    checks that attributes influencing array sizes need a default value
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
                    model_string=
                    """
                    // model
                    package types {
                        type int    as signed   with 32 bits
                        type UINT16 as unsigned with 16 bits
                        type float  as float    with 32 bits
                    }
                    package mypackage1 {
                    target_namespace "mypackage1.test"
                        struct Simple {
                            scalar n        : types.UINT16 {default="5"}
                            scalar x        : types.UINT16
                            array  a_ui16   : types.UINT16[n]
                        }
                    }
                    """)

    # ---------------------------
    # error 1
    # ---------------------------
    with raises(Exception, match=r'n.*needs to have a default value'):
        codegen.codegen(srcgen_folder=dest_folder,
                        model_string=
                        """
                        // model
                        package types {
                            type int    as signed   with 32 bits
                            type UINT16 as unsigned with 16 bits
                            type float  as float    with 32 bits
                        }
                        package mypackage1 {
                        target_namespace "mypackage1.test"
                            struct Simple {
                                scalar n        : types.UINT16 
                                scalar x        : types.UINT16
                                array  a_ui16   : types.UINT16[n]
                            }
                        }
                        """)

    #################################
    # END
    #################################

    # nothing generated: rmtree(dest_folder)
    assert not exists(dest_folder)
