from chope import element
from chope.css import css, rule

expected = \
"""<h1 color="yellow" size=123>
    text
    <h2>
        word
    </h2>
    <h3>
        letter
        space
    </h3>
</h1>"""


def test_should_render_nested_components_correctly():
    class h1(element):
        pass

    class h2(element):
        pass

    class h3(element):
        pass

    component = h1(color='yellow', size=123)[
        'text',
        h2[
            'word'
        ],
        h3[
            'letter',
            'space'
        ]
    ]

    assert component.render(4) == expected

def test_when_negative_number_is_passed_to_render_should_render_with_zero_indent():
    expected = "<a>\ntext\n</a>"

    class a(element):
        pass

    assert a['text'].render(-1) == expected

def test_able_to_render_css():
    expected = "<a>\n  b {\n    prop: text;\n  }\n</a>"

    class a(element):
        pass

    comp = a[
        css[
            'b': rule(prop='text')
        ]
    ]

    assert comp.render(2) == expected
