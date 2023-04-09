from chope.css import Css, Rule, px, rem, percent, in_

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
        'h1': Rule(
            color='red',
            font_size=rem/1.2,
            padding=in_/1,
            margin=percent/2,
            outline=(px/1, 'dotted', 'green')
        ),
        '.my-class': Rule(
            background='black'
        )
    ]

    assert style.render(3) == expected
