from chope.css import *

expected = '''h1 {
   color: red;
   font-size: 1.2rem;
   padding: 1em;
   outline: 1px dotted green;
}

.my-class {
   background: black;
}'''

def test_should_render_css_correctly():
    style = css[
        'h1': rule(
            color='red',
            font_size=rem/1.2,
            padding=em/1,
            outline=(px/1, 'dotted', 'green')
        ),
        '.my-class': rule(
            background='black'
        )
    ]

    assert style.render(3) == expected
