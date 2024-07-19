import pytest
from chope.css import Css, px, rem, percent, in_, RenderError
from chope.variable import Var

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

def test_set_variable_values():
    expected_render = 'h1 {color: red;padding: 1in;size: 5px;margin: 1%;}.my-class {background: black;}'
    expected_css = Css[
        'h1': dict(
            color=Var('color', 'red'),
            padding=Var('padding', in_/1),
            size=Var('size', Var('size_nested', px/5)),
            margin=Var('margin', percent/1)
        ),
        '.my-class': Var('my-class', {'background': 'black'})
    ]

    css = Css[
        # declaration variables
        'h1': dict(
            color=Var('color'),
            padding=Var('padding', in_/1),

            # nested variables
            size=Var('size', Var('size_nested', px/10)),
            margin=Var('margin', Var('margin_nested', percent/2))
        ),

        # rule variable
        '.my-class': Var('my-class')
    ]

    values = {
        'color': 'red',
        'size_nested': px/5,
        'margin': percent/1,
        'my-class': {'background': 'black'}
    }

    new_css = css.set_vars(values)

    assert new_css == expected_css
    assert new_css.render(indent=0) == expected_render

def test_handle_unset_rule_variable():
    css = Css[
        '.my-class': Var('my-class')
    ]

    with pytest.raises(RenderError):
        css.render()

def test_get_variable_names():
    expected = {'color', 'size', 'size_nested', 'my-class'}

    css = Css[
        'h1': dict(
            color=Var('color'),
            size=Var('size', Var('size_nested', px/10)),
        ),
        '.my-class': Var('my-class')
    ]

    assert css.get_vars() == expected
