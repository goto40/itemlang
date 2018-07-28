"""
simple editor for the model
WORK IN PROGRESS: 1%
"""

from __future__ import unicode_literals
import traceback
import itemlang.metamodel as custom_idl_metamodel
import codecs
import tkinter as tk
import sys
from textx.model import ObjCrossRef, ReferenceResolver
from textx import get_children_of_type
from textx.scoping import Postponed
import textx
import textx.scoping.tools as st
from arpeggio import Parser, Sequence, NoMatch, EOF, Terminal
from textx.exceptions import TextXSyntaxError, TextXSemanticError
from textx.const import MULT_OPTIONAL, MULT_ONE, MULT_ONEORMORE, \
    MULT_ZEROORMORE, RULE_ABSTRACT, RULE_MATCH, MULT_ASSIGN_ERROR, \
    UNKNOWN_OBJ_ERROR


if sys.version < '3':
    text = unicode  # noqa
else:
    text = str


def convert(value, _type):
    """
    Convert instances of textx types to python types.
    """
    return {
            'BOOL': lambda x: x == '1' or x.lower() == 'true',
            'INT': lambda x: int(x),
            'FLOAT': lambda x: float(x),
            'STRING': lambda x: x[1:-1].replace(r'\"',
                                                r'"').replace(r"\'", "'"),
            }.get(_type, lambda x: x)(value)


def parse_tree_to_objgraph(parser, parse_tree, file_name=None,
                           pre_ref_resolution_callback=None,
                           is_main_model=True):
    """
    Transforms parse_tree to object graph representing model in a
    new language.
    """

    metamodel = parser.metamodel

    if metamodel.textx_tools_support:
        pos_rule_dict = {}
    pos_crossref_list = []

    def process_match(nt):
        """
        Process subtree for match rules.
        """
        if isinstance(nt, Terminal):
            return convert(nt.value, nt.rule_name)
        else:
            # If RHS of assignment is NonTerminal it is a product of
            # complex match rule. Convert nodes to text and do the join.
            if len(nt) > 1:
                return "".join([text(process_match(n)) for n in nt])
            else:
                return process_match(nt[0])

    def process_node(node):
        if isinstance(node, Terminal):
            print("process_node TERMINAL: {} : {}".format(node, node.rule_name))
            from arpeggio import RegExMatch
            if metamodel.use_regexp_group and \
                    isinstance(node.rule, RegExMatch):
                if node.rule.regex.groups == 1:
                    value = node.extra_info.group(1)
                    return convert(value, node.rule_name)
                else:
                    return convert(node.value, node.rule_name)
            else:
                return convert(node.value, node.rule_name)

        assert node.rule.root, \
            "Not a root node: {}".format(node.rule.rule_name)
        # If this node is created by some root rule
        # create metaclass instance.
        inst = None
        if not node.rule_name.startswith('__asgn'):
            # If not assignment
            # Get class
            mclass = node.rule._tx_class

            if mclass._tx_type == RULE_ABSTRACT:
                # If this meta-class is product of abstract rule replace it
                # with matched concrete meta-class down the inheritance tree.
                # Abstract meta-class should never be instantiated.
                return process_node(node[0])
            elif mclass._tx_type == RULE_MATCH:
                # If this is a product of match rule handle it as a RHS
                # of assignment and return converted python type.
                return process_match(node)

            if parser.debug:
                parser.dprint("CREATING INSTANCE {}".format(node.rule_name))

            # If user class is given
            # use it instead of generic one
            if node.rule_name in metamodel.user_classes:
                user_class = metamodel.user_classes[node.rule_name]

                # Object initialization will be done afterwards
                # At this point we need object to be allocated
                # So that nested object get correct reference
                inst = user_class.__new__(user_class)

                # Initialize object attributes for user class
                parser.metamodel._init_obj_attrs(inst, user=True)
            else:
                # Generic class will call attributes init
                # from the constructor
                inst = mclass.__new__(mclass)

                # Initialize object attributes
                parser.metamodel._init_obj_attrs(inst)

            # Collect attributes directly on meta-class instance
            obj_attrs = inst

            inst._tx_position = node.position
            inst._tx_position_end = node.position_end

            # Push real obj. and dummy attr obj on the instance stack
            parser._inst_stack.append((inst, obj_attrs))

            for n in node:
                if parser.debug:
                    parser.dprint("Recursing into {} = '{}'"
                                  .format(type(n).__name__, text(n)))
                process_node(n)

            parser._inst_stack.pop()

            # If this object is nested add 'parent' reference
            if parser._inst_stack:
                if node.rule_name in metamodel.user_classes:
                    obj_attrs._txa_parent = parser._inst_stack[-1][0]
                else:
                    obj_attrs.parent = parser._inst_stack[-1][0]

            # If the class is user supplied we need to do
            # a proper initialization at this point.
            if node.rule_name in metamodel.user_classes:
                try:
                    # Get only attributes defined by the grammar as well
                    # as `parent` if exists
                    attrs = {}
                    if hasattr(obj_attrs, '_txa_parent'):
                        attrs['parent'] = obj_attrs._txa_parent
                        del obj_attrs._txa_parent
                    for a in obj_attrs.__class__._tx_attrs:
                        attrs[a] = getattr(obj_attrs, "_txa_%s" % a)
                        delattr(obj_attrs, "_txa_%s" % a)
                    inst.__init__(**attrs)
                except TypeError as e:
                    # Add class name information in case of
                    # wrong constructor parameters
                    e.args += ("for class %s" %
                               inst.__class__.__name__,)
                    parser.dprint(traceback.print_exc())
                    raise e

            # Special case for 'name' attrib. It is used for cross-referencing
            if hasattr(inst, 'name') and inst.name:
                # Objects of each class are in its own namespace
                if not id(inst.__class__) in parser._instances:
                    parser._instances[id(inst.__class__)] = {}
                parser._instances[id(inst.__class__)][inst.name] = inst

            if parser.debug:
                parser.dprint("LEAVING INSTANCE {}".format(node.rule_name))

        else:
            # Handle assignments
            attr_name = node.rule._attr_name
            op = node.rule_name.split('_')[-1]
            model_obj, obj_attr = parser._inst_stack[-1]
            cls = type(model_obj)
            metaattr = cls._tx_attrs[attr_name]

            # Mangle attribute name to prevent name clashing with property
            # setters on user classes
            if cls.__name__ in metamodel.user_classes:
                txa_attr_name = "_txa_%s" % attr_name
            else:
                txa_attr_name = attr_name

            if parser.debug:
                parser.dprint('Handling assignment: {} {}...'
                              .format(op, txa_attr_name))

            if op == 'optional':
                setattr(obj_attr, txa_attr_name, True)

            elif op == 'plain':
                attr_value = getattr(obj_attr, txa_attr_name)
                if attr_value and type(attr_value) is not list:
                    fmt = "Multiple assignments to attribute {} at {}"
                    raise TextXSemanticError(
                        message=fmt.format(
                            attr_name, parser.pos_to_linecol(node.position)),
                        err_type=MULT_ASSIGN_ERROR)

                # Convert tree bellow assignment to proper value
                value = process_node(node[0])

                if metaattr.ref and not metaattr.cont:
                    # If this is non-containing reference create ObjCrossRef
                    value = ObjCrossRef(obj_name=value, cls=metaattr.cls,
                                        position=node[0].position)
                    parser._crossrefs.append((model_obj, metaattr, value))
                    return model_obj

                if type(attr_value) is list:
                    attr_value.append(value)
                else:
                    setattr(obj_attr, txa_attr_name, value)

            elif op in ['list', 'oneormore', 'zeroormore']:
                for n in node:
                    # If the node is separator skip
                    if n.rule_name != 'sep':
                        # Convert node to proper type
                        # Rule links will be resolved later
                        value = process_node(n)

                        if metaattr.ref and not metaattr.cont:
                            # If this is non-containing reference
                            # create ObjCrossRef

                            value = ObjCrossRef(obj_name=value,
                                                cls=metaattr.cls,
                                                position=n.position)

                            parser._crossrefs.append((obj_attr, metaattr,
                                                      value))
                            continue

                        if not hasattr(obj_attr, txa_attr_name) or \
                                getattr(obj_attr, txa_attr_name) is None:
                            setattr(obj_attr, txa_attr_name, [])
                        getattr(obj_attr, txa_attr_name).append(value)
            else:
                # This shouldn't happen
                assert False

        # Collect rules for textx-tools
        if inst and metamodel.textx_tools_support:
            pos = (inst._tx_position, inst._tx_position_end)
            pos_rule_dict[pos] = inst

        return inst

    def call_obj_processors(metamodel, model_obj,
                            metaclass_of_grammar_rule=None):
        """
        Depth-first model object processing.
        """
        try:
            if metaclass_of_grammar_rule is None:
                metaclass_of_grammar_rule = \
                    metamodel[model_obj.__class__.__name__]
        except KeyError:
            raise TextXSemanticError(
                'Unknown meta-class "{}".'
                .format(model.obj.__class__.__name__))

        many = [MULT_ONEORMORE, MULT_ZEROORMORE]

        # return value of obj_processor
        return_value_grammar = None
        return_value_current = None

        # enter recursive visit of attributes only, if the class of the
        # object being processed is a meta class of the current meta model
        if model_obj.__class__.__name__ in metamodel:
            current_metaclass_of_obj = metamodel[model_obj.__class__.__name__]

            for metaattr in current_metaclass_of_obj._tx_attrs.values():
                # If attribute is base type or containment reference go down
                if metaattr.cont:
                    attr = getattr(model_obj, metaattr.name)
                    if attr:
                        if metaattr.mult in many:
                            for idx, obj in enumerate(attr):
                                if obj:
                                    result = call_obj_processors(metamodel,
                                                                 obj,
                                                                 metaattr.cls)
                                    if result is not None:
                                        attr[idx] = result
                        else:
                            result = call_obj_processors(metamodel,
                                                         attr, metaattr.cls)
                            if result is not None:
                                setattr(model_obj, metaattr.name, result)

            # call obj_proc of the current meta_class if type == RULE_ABSTRACT
            if current_metaclass_of_obj is not metaclass_of_grammar_rule:
                assert RULE_ABSTRACT == metaclass_of_grammar_rule._tx_type
                obj_processor_current = metamodel.obj_processors.get(
                    current_metaclass_of_obj.__name__, None)
                if obj_processor_current:
                    return_value_current = obj_processor_current(model_obj)

        # call obj_proc of rule found in grammar
        obj_processor_grammar = metamodel.obj_processors.get(
            metaclass_of_grammar_rule.__name__, None)
        if obj_processor_grammar:
            return_value_grammar = obj_processor_grammar(model_obj)

        # both obj_processors are called, if two different processors
        # are defined for the object metaclass and the grammar metaclass
        # (can happen with type==RULE_ABSTRACT):
        # e.g.
        #   Base: Special1|Special2;
        #   RuleCurrentlyChecked: att_to_be_checked=[Base]
        # with object processors defined for Base, Special1, and Special2.
        #
        # Both processors are called, but for the return value the
        # obj_processor corresponding to the object (e.g. of type Special1)
        # dominates over the obj_processor of the grammar rule (Base).
        #
        # The order they are called is: first object (e.g., Special1), then
        # the grammar based metaclass object processor (e.g., Base).
        if return_value_current is not None:
            return return_value_current
        else:
            return return_value_grammar  # may be None

    model = process_node(parse_tree)
    # Register filename of the model for later use (e.g. imports/scoping).
    is_primitive_type = False
    try:
        model._tx_filename = file_name
    except AttributeError:
        # model is some primitive python type (e.g. str)
        is_primitive_type = True
        pass

    if pre_ref_resolution_callback:
        pre_ref_resolution_callback(model)

    for scope_provider in metamodel.scope_providers.values():
        from textx.scoping import ModelLoader
        if isinstance(scope_provider, ModelLoader):
            scope_provider.load_models(model)

    if not is_primitive_type:
        model._tx_reference_resolver = ReferenceResolver(
            parser, model, pos_crossref_list)
        model._tx_parser = parser

    if is_main_model:
        from textx.scoping import get_all_models_including_attached_models
        models = get_all_models_including_attached_models(model)
        # filter out all models w/o resolver:
        models = list(filter(
            lambda x: hasattr(x, "_tx_reference_resolver"), models))

        resolved_count = 1
        unresolved_count = 1
        while unresolved_count > 0 and resolved_count > 0:
            resolved_count = 0
            unresolved_count = 0
            # print("***RESOLVING {} models".format(len(models)))
            for m in models:
                resolved_count_for_this_model, delayed_crossrefs = \
                    m._tx_reference_resolver.resolve_one_step()
                resolved_count += resolved_count_for_this_model
                unresolved_count += len(delayed_crossrefs)
            # print("DEBUG: delayed #:{} unresolved #:{}".
            #      format(unresolved_count,unresolved_count))
        if (unresolved_count > 0):
            error_text = "Unresolvable cross references:"

            for m in models:
                for _, _, delayed \
                        in m._tx_reference_resolver.delayed_crossrefs:
                    line, col = parser.pos_to_linecol(delayed.position)
                    error_text += ' "{}" of class "{}" at {}'.format(
                        delayed.obj_name, delayed.cls.__name__, (line, col))
            raise TextXSemanticError(error_text, line=line, col=col)

        for m in models:
            # TODO: what does this check?
            assert not m._tx_reference_resolver.parser._inst_stack

        # cleanup
        for m in models:
            del m._tx_reference_resolver

        # final check that everything went ok
        for m in models:
            assert 0 == len(get_children_of_type(Postponed.__class__, m))

            # We have model loaded and all link resolved
            # So we shall do a depth-first call of object
            # processors if any processor is defined.
            if m._tx_metamodel.obj_processors:
                if parser.debug:
                    parser.dprint("CALLING OBJECT PROCESSORS")
                for m in models:
                    call_obj_processors(m._tx_metamodel, m)

    if metamodel.textx_tools_support \
            and type(model) not in PRIMITIVE_PYTHON_TYPES:
        # Cross-references for go-to definition language server support
        # Already sorted based on ref_pos_start attr
        # (required for binary search)
        model._pos_crossref_list = pos_crossref_list

        # Dict for storing rules where key is position of rule instance in text
        # Sorted based on nested rules
        model._pos_rule_dict = OrderedDict(sorted(pos_rule_dict.items(),
                                                  key=lambda x: x[0],
                                                  reverse=True))
    return model


def edit(model_file):
    mm = custom_idl_metamodel.get_meta_model()
    #model = mm.model_from_file(model_file)

    with codecs.open(model_file, 'r', encoding='utf-8') as f:
        model_str = f.read()

    parser = mm._parser.clone()
    parser.parse(model_str, file_name = model_file)
    model = parse_tree_to_objgraph(
        parser, parser.parse_tree[0], file_name=model_file,
        pre_ref_resolution_callback=None,
        is_main_model=True)

    # GUI setup
    root = tk.Tk()
    SV = tk.Scrollbar(root, orient=tk.VERTICAL)
    SH = tk.Scrollbar(root, orient=tk.HORIZONTAL)
    T = tk.Text(root, height=4, width=50, wrap=tk.NONE)
    SV.pack(side=tk.RIGHT, fill=tk.Y)
    SH.pack(side=tk.BOTTOM, fill=tk.X)
    SV.config(command=T.yview)
    SH.config(command=T.xview)
    T.config(yscrollcommand=SV.set)
    T.config(xscrollcommand=SH.set)
    T.insert(tk.END, model_str)
    T.pack(fill=tk.BOTH, expand=1)

    # first test: color some aspects
    print("----------")


    # run GUI
    tk.mainloop()