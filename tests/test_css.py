from chope.css import Css, px, rem, percent, in_

expected = '''h1 {
   color: red;
   font-size: 1.2rem;
   padding: 1in;
   margin: 2%;
   outline: 1px dotted green;
}

.my-class {
   background: black;
}'''


def test_should_render_css_correctly():
    style = Css[
        'h1': dict(
            color='red',
            font_size=rem/1.2,
            padding=in_/1,
            margin=percent/2,
            outline=(px/1, 'dotted', 'green')
        ),
        '.my-class': dict(
            background='black'
        )
    ]

    assert style.render(3) == expected

def test_when_indent_is_zero_should_render_flat_string():
    expected = 'a {b: c;}d {e: f;}'

    style = Css['a': dict(b='c'), 'd': dict(e='f')]

    assert style.render(0) == expected
