# Chope

CSS &amp; HTML on Python Easily.

![PyPI](https://img.shields.io/pypi/v/chope)
![Pepy Total Downlods](https://img.shields.io/pepy/dt/chope)
![GitHub](https://img.shields.io/github/license/hanstjua/chope)
![GitHub Workflow Status (with branch)](https://img.shields.io/github/actions/workflow/status/hanstjua/chope/run_tests.yml?branch=main)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/chope?label=python)

Chope is a library that aims to provide a HTML and CSS domain-specific language (DSL) for Python.
It draws inspiration from Clojure's [Hiccup](https://github.com/weavejester/hiccup) and JavaScript's [Emotion](https://emotion.sh/docs/introduction).

## Install

Chope can be installed through pip.

`pip install chope`
    
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

### HTML

Declaring an element is as simple as this:

```python
# <div>content</div>

div['content']
```

Element attributes can be specified like so:

```python
# <div id="my-id" class="my-class your-class">content</div>

div(id='my-id', class_='my-class your-class')['content']
```

Notice the `_` suffix in the `class_` attribute. This suffix is necessary for any attribute names that clashes with any Python keyword.

You can also define `id` and `class` using CSS selector syntax:

```python
# <div id="my-id" class="my-class your-class" title="Title">content</div>

div('#my-id.my-class.your-class', title='Title')['content']
```

Iterables can be used to generate a sequence of elements in the body of an element.

```python
# <ul><li>0</li><li>1</li><li>2</li></ul>

ul[
    (li[str(i)] for i in range(3))
]
```

#### Creating custom elements

If you want to create a custom element with a custom tag, simply inherit from the `Element` class.

```python
from chope import Element


class custom(Element):  ## class name will be used as tag name during rendering
    pass


custom['some content.']  ## <custom>some content.</custom>
```

Normally, you don't need to override any method of `Element`, but if you want to change how your element is rendered, you can override the `render()` method.

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
