from chope import Element
from chope.css import Css, Rule

expected = \
"""<e1 class="my-class" color="yellow" size=123>
    text
    <e2>
        word
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

    component = e1(class_='my-class', color='yellow', size=123)[
        'text',
        e2[
            'word'
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
