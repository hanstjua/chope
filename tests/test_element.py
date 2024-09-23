from typing import Tuple

import pytest

from chope import Element
from chope.css import Css
from chope.element import DuplicateAttributeError
from chope.variable import Var


class a(Element):
    pass


class b(Element):
    pass


def test_should_render_nested_components_correctly():
    class e1(Element):
        pass

    class e2(Element):
        pass

    class e3(Element):
        pass

    expected = """<e1 class="my-class" color="yellow" size=123 my-attr="yes" autofocus>
    text
    <e2>
        word<br>
    </e2>
    <e3>
        letter
        space
        symbols
    </e3>
</e1>"""

    component = e1(
        class_="my-class", color="yellow", size=123, my_attr="yes", autofocus=True
    )["text", e2["word\n"], e3["letter", ["space", "symbols"]]]

    assert component.render(4) == expected


@pytest.mark.parametrize(
    "selectors, tuple, kv, expected",
    (
        ("#id.class1.class2", (), {}, 'id="id" class="class1 class2"'),
        ("", ("my[attr]", "x"), {}, 'my[attr]="x"'),
        ("", (), {"named": 1.0}, "named=1.0"),
        ("#id", ("my-attr", "x"), {}, 'id="id" my-attr="x"'),
        ("", ("my@attr", 1), {"named": 1.0}, "my@attr=1 named=1.0"),
        ("#id", (), {"named": 1.0}, 'id="id" named=1.0'),
        ("#id", ("my.attr", 1), {"named": 1.0}, 'id="id" my.attr=1 named=1.0'),
    ),
    ids=[
        "selectors only",
        "tuple only",
        "key-value only",
        "selector + tuple",
        "tuple + key-value",
        "selector + key-value",
        "all",
    ],
)
def test_attribute_definitions_styles(
    selectors: str, tuple: Tuple[str, ...], kv: dict, expected: str
):
    args = (selectors,) + tuple if selectors else tuple
    assert a(*args, **kv).render(0) == f"<a {expected}></a>"


@pytest.mark.parametrize(
    "selector, tuple, kv",
    (
        ("#id", ("id", "di"), {}),
        ("#id", (), {"id": "di"}),
        ("", ("id", "id"), {"id": "di"}),
        ("#id", ("id", "di"), {"id": "di"}),
    ),
    ids=["selector + tuple", "selector + key-value", "tuple + key-value", "all"],
)
def test_conflicting_attribute_definitions_should_raise_error(
    selector: str, tuple: Tuple[str, ...], kv: dict
):
    with pytest.raises(DuplicateAttributeError):
        args = (selector,) + tuple if selector else tuple
        a(*args, **kv).render(0)


def test_zero_indent_should_render_flat_string():
    expected = "<a>text</a>"

    assert a["text"].render(0) == expected


def test_when_negative_number_is_passed_to_render_should_render_with_zero_indent():
    assert a["text"].render(-1) == a["text"].render(0)


def test_able_to_render_css():
    expected = "<a>\n  b {\n    prop: text;\n  }\n</a>"

    comp = a[Css["b" : dict(prop="text")]]

    assert comp.render(2) == expected


def test_infer_id_and_classes_through_css_selector():
    expected = '<a id="id" class="class1 class2 class3 class4">text</a>'

    assert a("#id.class1.class2", class_="class3 class4")["text"].render(0) == expected


def test_should_raise_exception_if_id_detected_in_both_kwargs_and_css_selector():
    with pytest.raises(DuplicateAttributeError):
        a("#a", id="a")


def test_override_element_attributes():
    expected_comp = a(name='content', id='overriden', some_attr='new')['Content']

    comp = a(name='content', id='original', some_attr='old')['Content']

    assert comp(id='overriden', some_attr='new').render() == expected_comp.render()


def test_set_variable_values():
    expected_render = '<a id="id" count=1>Outer<a name="default"><b name="inner">Inner</b></a><a>set_nested</a><a><a>set_nested</a></a><a>set_nested</a></a>'
    expected_comp = a(id=Var("id", "id"), count=Var("count", 1))[
        Var("outer", "Outer"),
        a(name=Var("name", "default"))[
            Var("inner", b(name="inner")[
                "Inner"
            ])
        ],
        Var("unset_nested", Var("set_nested", a["set_nested"])),
        Var("unset_nested", a[Var("set_nested", a["set_nested"])]),
        Var("set_nested", a["set_nested"]),
    ]

    comp = a(id=Var("id"), count=Var("count"))[
        # variable in element
        Var("outer"),

        # variable in inner element
        a(name=Var("name", "default"))[
            Var("inner")
        ],

        # nested variables
        Var("unset_nested", Var("set_nested")),

        # nested variable inside element
        Var("unset_nested", a[Var("set_nested")]),
        Var("set_nested", a[Var("unset_nested")]),
    ]

    values = {
        "id": "id",
        "count": 1,
        "outer": "Outer",
        "inner": b(name="inner")["Inner"],
        "set_nested": a["set_nested"],
    }

    new_comp = comp.set_vars(values)

    assert new_comp == expected_comp
    assert new_comp.render(indent=0) == expected_render


def test_set_variable_values_using_kwargs():
    expected_comp = a(name=Var("name", "my-name"))[
        Var("content", "My content."), 
        b[Var("inner", "Inner content.")]
    ]

    comp = a(name=Var("name"))[
        Var("content"), 
        b[Var("inner")]
    ]

    new_comp = comp.set_vars(
        {"name": "not-my-name"},
        name="my-name",
        content="My content.",
        inner="Inner content.",
    )

    assert new_comp == expected_comp


def test_set_variables_to_iterables():
    equivalent_comp = a[
        b['0'],
        b['1'],
        b['2'],
        b['3'],
        b['4']
    ]

    expected = equivalent_comp.render()

    comp = a[
        Var('content'),
        (b['3'], b['4'])
    ]

    result = comp.set_vars(content=(b[str(i)] for i in range(3))).render()

    assert result == expected


def test_get_variable_names():
    vars_count = 5
    vars = [Var(str(i)) for i in range(vars_count)]

    comp = a(var=vars[0])[
        vars[1],
        a(var=vars[1])[
            vars[2],
            # nested variables
            Var("0", vars[3]),
            Var("0", a[vars[4]]),
        ],
    ]

    expected = {str(i) for i in range(vars_count)}

    assert comp.get_vars() == expected

def test_able_to_accept_empty_iterable_as_a_child():
    comp = a[
        b[[]],
        b[()],
        b[(i for i in range(0))]
    ]
    expected = '<a><b></b><b></b><b></b></a>'

    assert comp.render(0) == expected
