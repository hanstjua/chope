# Chope

CSS &amp; HTML on Python Easily.

![PyPI](https://img.shields.io/pypi/v/chope)
![Pepy Total Downlods](https://img.shields.io/pepy/dt/chope)
![GitHub](https://img.shields.io/github/license/hanstjua/chope)
![GitHub Workflow Status (with branch)](https://img.shields.io/github/actions/workflow/status/hanstjua/chope/run_tests.yml?branch=main)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/chope?label=python)

Chope is a library that aims to provide a HTML and CSS domain-specific language (DSL) for Python.
It draws inspiration from Clojure's [Hiccup](https://github.com/weavejester/hiccup) and JavaScript's [Emotion](https://emotion.sh/docs/introduction).

## Table of Contents
* [Install](#install)
* [Syntax](#syntax)
    * [HTML](#html)
        * [Creating Custom Elements](#creating-custom-elements)
    * [CSS](#css)
        * [Units](#units)
* [Render](#render)
* [Building a Template](#building-a-template)
    * [Factory Function](#factory-function)
    * [Variable Object](#variable-object)

<a name="install" />

## Install

Chope can be installed through pip.

`pip install chope`

<a name="syntax" />

## Syntax

Here is a basic example of Chope syntax:

```python
from chope import *
from chope.css import *

page = html[
    head[
        style[
            Css[
                'body': dict(
                    background_color='linen',
                    font_size=pt/12
                ),
                '.inner-div': dict(
                    color='maroon',
                    margin_left=px/40
                )
            ]
        ]
    ],
    body[
        h1['Title'],
        div(class_='outer-div')[
            div(class_='inner-div')[
                'Some content.'
            ]
        ]
    ]
]
```

<a name="html" />

### HTML

Declaring an element is as simple as this:

```python
# <div>content</div>

div['content']
```

Element attributes can be specified like so:

```python
# <div id="my-id" class="my-class your-class">This is key-value style.</div>

div(id='my-id', class_='my-class your-class')['This is key-value style.']
```

Notice the `_` suffix in the `class_` attribute. This suffix is necessary for any attribute names that clashes with any Python keyword.

You can also define `id` and `class` using CSS selector syntax:

```python
# <div id="my-id" class="my-class your-class" title="Title">This is selector style.</div>

div('#my-id.my-class.your-class', title='Title')['This is selector style.']
```

For attributes with names that cannot be declared using the *key-value* style, you can use the *tuple* style.

```python
# <div my:attr="x" ur-attr="y" their[attr]="z">This is tuple style.</div>

div('my:attr', 'x',
    'ur-attr', 'y',
    'their[attr]', 'z')[
        'This is tuple style.'
    ]
```

The different styles can be mixed as long as there is no duplicate attribute definition.

```python
# acceptable mixed style

div('#my-id.class1.class2',
    'my:attr', 'x',
    'ur-attr', 'y',
    'their[attr]', 'z',
    title="Mix 'em up",
    subtitle="But don't get mixed up"
    )[
        'This mixed style is OK.'
    ]

# NOT acceptable mixed style

div('#my-id.class1.class2',
    'id', 'x',  # conflicts with 'id' defined in selector style
    'title', 'y',
    'their[attr]', 'z',
    title="Mix 'em up",  # conflicts with 'title' defined in tuple style
    subtitle="But don't get mixed up"
    )[
        'This mixed style is NOT OK.'
    ]
```

Iterables can be used to generate a sequence of elements in the body of an element.

```python
# <ul><li>0</li><li>1</li><li>2</li></ul>

ul[
    [li[str(i)] for i in range(3)]
]
```

<a name="creating-custom-elements" />

#### Creating Custom Elements

If you want to create a custom element with a custom tag, simply inherit from the `Element` class.

```python
from chope import Element


class custom(Element):  ## class name will be used as tag name during rendering
    pass


custom['some content.']  ## <custom>some content.</custom>
```

Normally, you don't need to override any method of `Element`, but if you want to change how your element is rendered, you can override the `render()` method.

<a name="css" />

### CSS

The CSS syntax in Chope is simply a mapping between CSS selector strings and declarations dictionaries.

Here's how a simple CSS stylesheet looks like in Chope:

```python
'''
h1 {
    color: blue;
}

.my-class {
    background-color: linen;
    text-align: center;
}
'''

Css[
    'h1': dict(
        color='blue'
    ),
    '.my-class': dict(
        background_color='linen',
        text_align='center'
    )
]

# OR

Css[
    'h1': {
        'color': 'blue'
    },
    '.my-class': {
        'background-color': 'linen',
        'text-align': 'center'
    }
]
```

When you do declarations using the `dict` constructor, any `_` will be converted to `-` automatically.

If your attribute name actually contains an `_`, declare using dictionary literal instead.

<a name="units" />

#### Units

Declaring size properties is very simple:

```python
'''
.my-class {
    font-size: 14px;
    margin: 20%;
}
'''

Css[
    '.my-class': dict(
        font_size=px/14,
        margin=percent/20
    )
]
```

Chope supports standard HTML units. (e.g.`em`, `rem`, `pt`, etc.)

To set properties with multiple values, simply pass an iterable or a string.

```python
'''
.my-class {
    padding: 58px 0 0;
}
'''

Css[
    '.my-class': dict(
        padding=(px/58, 0, 0)
    )
]

# OR

Css[
    '.my-class': dict(
        padding='58px 0 0'
    )
]
```

<a name="render" />

## Render

Once you are done defining your CSS and HTML, you can render them into string using the `render()` method.

```python
>>> page = html[
    head[
        style[
            Css[
                '.item': dict(font_size=px/14)
            ]
        ]
    ],
    body[
        div('#my-item.item')['My content.']
    ]
]
>>> print(page.render())
'<html>
  <head>
    <style>
      .item {
        font-size: 14px;
      }
    </style>
  </head>
  <body>
    <div id="my-item" class="item">
      My content.
    </div>
  </body>
</html>'
```

By default, `render()` will add indentations with 2 spaces. You can modify this using the `indent` keyword argument.

```python
>>> print(page.render(indent=4))
'<html>
    <head>
        <style>
            .item {
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div id="my-item" class="item">
            My content.
        </div>
    </body>
</html>'
>>> print(page.render(indent=0))  ## render flat string
'<html><head><style>.item {font-size: 14px;}</style></head><body><div id="my-item" class="item">My content.</div></body></html>'
```

CSS objects can also be rendered the same way.

```python
>>> css = Css[
    'h1': dict(font_size=px/14),
    '.my-class': dict(
        color='blue',
        padding=(0,0,px/20)
    )
]
>>> print(css.render())
'h1 {
    font-size: 14px;
}

.my-class {
    color: blue;
    padding: 0 0 20px;
}'
```

<a name="building-a-template" />

## Building a Template

There are different ways you can construct a HTML template with `chope`, two of which are *Factory Function* and *Variable Object*.

<a name="factory-function" />

### Factory Function

Factory function is probably the simplest way to build reusable templates.

```python
def my_list(title: str, items: List[str], ordered: bool = False) -> div:
    list_tag = ol if ordered else ul
    return div[
        f'{title}<br>',
        list_tag[
            [li[i] for i in items]
        ]
    ]

def my_content(items: List[Component], attrs: dict) -> div:
    return div(**attrs)[
        items
    ]

result = my_content(
    [
        my_list('Grocery', ['Soap', 'Shampoo', 'Carrots']),
        my_list(
            'Egg Cooking', 
            ['Crack egg.', 'Fry egg.', 'Eat egg.'],
            ordered=True
        )
    ],
    {
        'id': 'my-content',
        'class': 'list styled-list'
    }
)
```

Factory function is a simple, elegant solution to construct a group of small, independent reusable templates. However, when your templates group grows in size and complexity, the factory functions can get unwieldy, as we will see at the end of the next section.

<a name="variable-object" />

### Variable Object

Another way to build a HTML template is to use the *Variable Object*, `Var`.


```python
from chope import *
from chope.variable import Var

# declaring element with Var content
template = html[
    div[Var('my-content')]
]

# setting value to Var object

final_html = template.set_vars({'my-content': 'This is my content.'})  ## dict style

## OR

final_html = template.set_vars(my_content='This is my content.')  ## key-value style

print(final_html.render(indent=0))  ## <html><div>This is my content.</div></html>
```

You can combine both _dict_ and _key-value_ style when setting variable values, but note that **values defined using _kwargs_ take priority over those defined using _dict_**.

A variable object can have a default value.

```python
>>> print(div[Var('content', 'This is default content.')].render(indent=0))
'<div>This is default content.</div>'
```

A variable object's value can be set to an element.

```python
>>> content = div[Var('inner')]
>>> new_content = content.set_vars(inner=div['This is inner content.'])
>>> print(new_content.render())
'<div>
  <div>
    This is inner content.
  </div>
</div>'
```

`Var` works in an element attribute as well.

```python
>>> content = div(name=Var('name'))['My content.']
>>> new_content = content.set_vars(name='my-content')
>>> print(new_content.render())
'<div name="my-content">
  My content.
</div>'
```

You can use `Var` in CSS too.

```python
>>> css = Css[
    # CSS rule as a variable
    'h1': dict(font_size=Var('h1.font-size')),

    # CSS declaration as a variable
    '.my-class': Var('my-class')
]
>>> new_css = css.set_vars({'h1.font-size': px/1, 'my-class': {'color': 'blue'}})
>>> print(new_css.render())
'h1 {
  font-size: 1px;
}

.my-class {
  color: blue;
}'
```

The `set` of all variable names in an element/CSS can be retrieved using the `get_vars()` method.

```python
>>> template = html[
    style[
        Css[
            'h1': dict(font_size=Var('css.h1.font-size'))
        ]
    ],
    div[
        Var('main-content'),
        div[
            Var('inner-content')
        ]
    ]
]
>>> print(template.get_vars())
{'main-content', 'inner-content', 'css.h1.font-size'}
```

An advantage of using variable object is that it allows for easy deferment of variable value settings, which makes combining templates simple.

```python
navs_template = ul('.nav')[
    Var('navs.items')
]

pagination_template = nav[
    ul('.pagination')[
        li('.page-item', class_=Var(
            'pagination.previous.disabled',
            'disabled'
        ))['Previous'],
        Var('nav.pages'),
        li('.page-item', class_=Var(
            'pagination.next.disabled',
            'disabled'
        ))['Next']
    ]
]

body_template = body[
    navs_template,
    div('.main-content')[Var('body.main-content')],
    pagination_template
]
```

Compare that to the equivalent factory function implementation.

```python
def navs_template(items: List[li]) -> ul:
    return ul('.nav')[
        items
    ]

def pagination_template(
    pages: List[li],
    previous_disabled: bool = True,
    next_disabled: bool = True
) -> nav:
    return nav[
        ul('.pagination')[
            li(f'.page-item{" disabled" if previous_disabled else ""}')['Previous'],
            pages,
            li(f'.page-item{" disabled" if next_disabled else ""}')['Next']
        ]
    ]

def body_template(
    navs_items: List[li],
    pagination_pages: List[li],
    body_main_content: Element,
    pagination_previous_disabled: bool = True,
    pagination_next_disabled: bool = True
) -> body:
    return body[
        navs_template(navs_items),
        body_main_content,
        pagination_template(
            pagination_pages,
            pagination_previous_disabled,
            pagination_next_disabled
        )
    ]
```

As you may have observed, the number of parameters for upstream template's factory function can easily explode when you start combining more downstream templates.
