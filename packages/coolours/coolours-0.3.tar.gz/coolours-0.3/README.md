# **Coolours**
### A Python Module To Make Text Colouring Easy
#### _Made By Alex Hawking_

# Installation

> ## With Pip

Install with:

    pip install coolours

or

    pip install coolours

> ## With wget

_Wget must be installed_

    cd ~/Library/Python/3.7/lib/python/site-packages && wget https://raw.githubusercontent.com/Handmade-Studios/coolours-module/master/coolours/coolours.py && cd ~

Probably easier to copy and paste that ^


# Usage

> ## Importing

Import coolours using:

    from coolours.coolours import *

You can import with

    import coolours.coolours

But that requires you to use `print(coolours.colour('style', 'textcolour', 'backgroundcolour'))`, so I think it is easier to use the first method.

> ## Colours

You use coolours within the `print` function as shown below:

    print(colour('style', 'text-colour', 'background-colour') + 'your text')

**Make sure you place the colours and styles within quotes**

> ## Default

To make the colours back to default after the coloured text add `default` to the end of the print function:

    print(colour('style', 'text-colour', 'background-colour') + 'your text' + default)

> ## Updating

To update use:

    pip install --upgrade coolours

# List of Colours

### Coolors contains the following colours:

> ## Styles

- none
- bold
- underline (not supported in all temrinals)
- blink (not supported in all terminals)

> ## Text Colours

- none
- black
- red
- green
- yellow
- blue
- purple
- cyan
- white
- brightblack
- brightred
- brightgreen
- brightyellow
- brightblue
- brightpurple
- brightcyan
- brightwhite

> ## Background Colours

- none
- black
- red
- green
- yellow
- blue
- purple
- cyan
- white
- brightblack
- brightred
- brightgreen
- brightyellow
- brightblue
- brightpurple
- brightcyan
- brightwhite


# Future

More colours and styles coming soon. Will also add a way to align text.


