from __future__ import absolute_import
from __future__ import unicode_literals

from os.path import dirname, exists
from shutil import rmtree
import os.path
from pytest import raises


def test_validation_check_array_attribute():
    """
    checks that array length depends not on attributes defined after the array in the struct.
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
                        type int as custom {}
                        type UINT16 as custom {}
                        type float as custom {}
                    }
                    package mypackage1 {
                    target_namespace "mypackage1.test"
                    struct Header {
                        scalar proofword : types.int
                        scalar N : types.int { default = "0x16" }
                        scalar k : types.int
                        array info : types.float[10]
                    }
                    struct Simple {
                        scalar h        : Header
                        scalar n        : types.UINT16 {default="5"}
                        scalar x        : types.UINT16
                        array  a_ui16   : types.UINT16[n]
                    }
                    }
                    """)

    # ---------------------------
    # array size after array (1)
    # ---------------------------
    with raises(Exception, match=r'depends on .* not defined before it'):
        codegen.codegen(srcgen_folder=dest_folder,
                        model_string=
                        """
                        // model
                        package types {
                            type int as custom {}
                            type UINT16 as custom {}
                            type float as custom {}
                        }
                        package mypackage1 {
                        target_namespace "mypackage1.test"
                        struct Header {
                            scalar proofword : types.int
                            scalar n : types.int { default = "0x16" }
                            scalar k : types.int
                            array info : types.float[10]
                        }
                        struct Simple {
                            scalar h        : Header
                            scalar x        : types.UINT16
                            array  a_ui16   : types.UINT16[n]
                            scalar n        : types.UINT16 {default="5"} // error
                        }
                        }
                        """)

    # ---------------------------
    # array size after array (2)
    # ---------------------------
    with raises(Exception, match=r'depends on .* not defined before it'):
        codegen.codegen(srcgen_folder=dest_folder,
                        model_string=
                        """
                        // model
                        package types {
                            type int as custom {}
                            type UINT16 as custom {}
                            type float as custom {}
                        }
                        package mypackage1 {
                        target_namespace "mypackage1.test"
                        struct Header {
                            scalar proofword : types.int
                            scalar n : types.int { default = "0x16" }
                            scalar k : types.int
                            array info : types.float[10]
                        }
                        struct Simple {
                            scalar n        : types.UINT16 {default="5"} 
                            scalar x        : types.UINT16
                            array  a_ui16   : types.UINT16[n:x][h.n:y]
                            scalar h        : Header
                        }
                        }
                        """)

    #################################
    # END
    #################################

    # nothing generated: rmtree(dest_folder)
    assert not exists(dest_folder)
