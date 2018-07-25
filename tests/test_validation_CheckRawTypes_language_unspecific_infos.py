from __future__ import absolute_import
from __future__ import unicode_literals

from os.path import dirname, exists
from shutil import rmtree
import os.path
from pytest import raises


def test_validation_check_raw_types():
    """
    checks that addon info for used types for specific languages are defined.
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
                    model_string=
                    """
                    // model
                    package types {
                        type intA as custom { }
                        type intB as custom with 32 bits { }
                        type intC as signed with 32 bits { }
                        type uintD as unsigned with 32 bits { }
                        type floatE as float with 32 bits {}
                    }
                    """)

    # ---------------------------
    # error 1
    # ---------------------------
    with raises(Exception, match=r'Bits need to be specified for intC'):
        codegen.codegen(srcgen_folder=dest_folder,
                        model_string=
                        """
                        // model
                        package types {
                            type intA as custom { }
                            type intB as custom with 32 bits { }
                            type intC as signed { }
                            type uintD as unsigned with 32 bits { }
                            type floatE as float with 32 bits {}
                        }
                        """)

    # ---------------------------
    # error 2
    # ---------------------------
    with raises(Exception, match=r'Bits need to be specified for uintD'):
        codegen.codegen(srcgen_folder=dest_folder,
                        model_string=
                        """
                        // model
                        package types {
                            type intA as custom { }
                            type intB as custom with 32 bits { }
                            type intC as signed with 32 bits { }
                            type uintD as unsigned { }
                            type floatE as float with 32 bits {}
                        }
                        """)

    # ---------------------------
    # error 3
    # ---------------------------
    with raises(Exception, match=r'Bits need to be specified for floatE'):
        codegen.codegen(srcgen_folder=dest_folder,
                        model_string=
                        """
                        // model
                        package types {
                            type intA as custom { }
                            type intB as custom with 32 bits { }
                            type intC as signed with 32 bits { }
                            type uintD as unsigned with 32 bits { }
                            type floatE as float {}
                        }
                        """)

    #################################
    # END
    #################################

    # no struct to be generated: rmtree(dest_folder)
    assert not exists(dest_folder)
