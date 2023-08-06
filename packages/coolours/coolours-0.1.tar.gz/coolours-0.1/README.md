# **Coolours**
### A Python Module To Make Text Colouring Easy
#### _Made By Alex Hawking_


# Usage

> ## Importing

Import coolours using:

    from coolours import *

You can import with

    import coolours

But that requires you to use `print(coolours.colour('style', 'textcolour', 'backgroundcolour'))`, so I think it is easier to use the first method.

> ## Colours

You use coolours within the `print` function as shown below:

    print(colour('style', 'text-colour', 'background-colour') + 'your text')

**Make sure you place the colours and styles within quotes**

> ## Default

To make the colours back to default after the coloured text add `default` to the end of the print function:

    print(colour('style', 'text-colour', 'background-colour') + 'your text' + default)

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


