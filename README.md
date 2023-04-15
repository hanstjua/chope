# Chope

CSS &amp; HTML on Python Easily.

![PyPI](https://img.shields.io/pypi/v/chope)
![GitHub](https://img.shields.io/github/license/hanstjua/chope)
![GitHub Workflow Status (with branch)](https://img.shields.io/github/actions/workflow/status/hanstjua/chope/run_tests.yml?branch=main)

Chope is a library that aims to provide a HTML and CSS domain-specific language (DSL) for Python.
It draws inspiration from Clojure's [Hiccup](https://github.com/weavejester/hiccup) and [Emotion](https://emotion.sh/docs/introduction).

## Install

Chope can be installed throough pip.

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
                'Some content.
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
