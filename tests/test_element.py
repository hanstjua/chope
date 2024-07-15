import pytest
from chope import Element
from chope.css import Css
from chope.variable import Var

expected = \
"""<e1 class="my-class" color="yellow" size=123 autofocus>
    text
    <e2>
        word<br>
    </e2>
    <e3>
        letter
        space
    </e3>
</e1>"""


def test_should_render_nested_components_correctly():
    class e1(Element):
        pass

    class e2(Element):
        pass

    class e3(Element):
        pass

    component = e1(class_='my-class', color='yellow', size=123, autofocus=True)[
        'text',
        e2[
            'word\n'
        ],
        e3[
            'letter',
            'space'
        ]
    ]

    assert component.render(4) == expected

def test_zero_indent_should_render_flat_string():
    expected = "<a>text</a>"

    class a(Element):
        pass

    assert a['text'].render(0) == expected

def test_when_negative_number_is_passed_to_render_should_render_with_zero_indent():
    class a(Element):
        pass

    assert a['text'].render(-1) == a['text'].render(0)

def test_able_to_render_css():
    expected = '<a>\n  b {\n    prop: text;\n  }\n</a>'

    class a(Element):
        pass

    comp = a[
        Css[
            'b': dict(prop='text')
        ]
    ]

    assert comp.render(2) == expected

def test_infer_id_and_classes_through_css_selector():
    expected = '<a id="id" class="class1 class2 class3 class4">text</a>'

    class a(Element):
        pass

    assert a('#id.class1.class2', class_='class3 class4')['text'].render(0) == expected

def test_should_raise_exception_if_id_detected_in_both_kwargs_and_css_selector():
    class a(Element):
        pass

    with pytest.raises(ValueError):
        a('#a', id='a')

def test_set_variable_values():
    expected = '<a id="id" count=1>Outer<a name="default"><b name="inner">Inner</b></a></a>'

    class a(Element):
        pass

    class b(Element):
        pass

    comp = a(id = Var('id'), count = Var('count'))[
        Var('outer'),
        a(name = Var('name', 'default'))[
            Var('inner')
        ]
    ]

    values = {
        'id': 'id',
        'count': 1,
        'outer': 'Outer',
        'inner': b(name='inner')['Inner']
    }

    new_comp = comp.set_vars(values)
    
    assert new_comp.render(indent=0) == expected
