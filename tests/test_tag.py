from chope import tag

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
    class h1(tag):
        pass

    class h2(tag):
        pass

    class h3(tag):
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

    class a(tag):
        pass

    assert a['text'].render(-1) == expected
