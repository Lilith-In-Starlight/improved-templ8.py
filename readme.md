# templ8.py

templ8.py (or just templ8) is a templating software for websites designed with lightweightness, flexibility and ease of use in mind. It was also designed with the idea being that one's website is one's temple, so a lot of the terminology is thematic with that.

The previous version, which I call templ8.0 was extremely tedious to use and designed only for me. This one is an improvement in those regards (not that it being designed for my own projects makes it bad, but it'd be cool to make it generalizable).

It uses textile instead of markdown simply because I personally like it more. Soon, it'll support markdown too.

It's currently being made, so I don't expect this to be functional or fully usable. And the code is bad. It will probably remain bad, but I'll try to make it okay over time.

## Roadmap
*Or, i try to pretend i have an organized plan for this project (i dont)*

This roadmap is as chronologically ordered as homestuck (i'm _pretty sure_ that it isn't ordered but honestly good luck.)

- [x] Basic templating functionality like templ8.0's
- [x] Easier-to-customize replacement tags
- [x] Copy non-markup files from the input folder into the output
- [x] txignore file for textile files that should be put on the output folder unprocessed
- [x] Customizing "core" file and directory names of a project
- [ ] Change a specific page's basehtml
- [ ] Markdown support (with mdignore)
- [ ] IFKEYs for further basetemplate flexibility
- [X] Blogging
- [ ] RSS and ASS feed generating tool

## Crash Course
*Or, i try so fucking hard to make this program make sense*

### Commands
templ8 currently has two commands:

- `genesis [dirname]`: Creates a new directory named `[dirname]` with basic files required for templ8's functionality. Only useful if templ8 is in PATH on environment variables.
- `divine`: Assembles the current project into a website in the output folder. Requires a `d8y` file to be in the current directory. It also copies non-textile files to the output.
- `radio`: Assembles a blog. It's the worst blogging tool you have ever seen. I won't even document it here, I'll document it on my website later. It's too tedious for a readme.

### How does it work?
Put the templ8.py file in an empty folder. Make a file called `d8y` with no extension, a file called `basehtml`, also with no extension, and two folders, `input` and `output`.

You might also want one called `repl8ce`, with no extension.

The `basehtml` file is an html file in which templ8.py puts the content of your pages. It tells templ8 how your page should look: Whatever you put in it, will be there in every page.

Somewhere in `basehtml`'s body should be a line that only says `##CONTENT##`. This is what templ8 will replace for the content.

```textile
/input/index.textile

example paragraph with some html stuff
```


```html
/basehtml

<html>
  <body>
     ##CONTENT##
  </body>
</html>
```

```html
/output/index.html

<html>
  <body>
     <p>example paragraph with some html stuff</p>
  </body>
</html>
```

#### Custom Replacement Keys

You can create custom `##KEYS##` in `rpl8cmnt`. They're parts of the basehtml that individual files can modify.

```plaintext
/repl8ce

PAGETITLE=A Default Title
CUSTOMKEY=Another default value
EMPTYKEY
```

EMPTYKEY's default value is an empty string.

```html
/basehtml

...
<head>
<title>##PAGETITLE##</title>
</head>
...
```


```plaintext
/input/index.html

CUSTOMKEY=Non Default Value
-BEGINFILE-
the page's contents start here
```

```html
/output/index.html

...
<head>
<title>Non Default Value</title>
</head>
...
```

A custom key can be replaced with an empty string by doing `CUSTOMKEY=` with nothing after the equals.

#### Core Renaming
You can also rename the input, output, basehtml and repl8ce files using the d8y file. Simply do this, making sure your custom values don't start with a number and dont have spaces:

```plaintext
input=your_input_folder
output=your_output_folder
replace=your_replace_file
basehtml=your_basehtml_file
```

#### txignore
txignore files are like .gitignore files, except they don't mean "don't put this file on the ouput," it's more like "output the raw file." Putting a path to a directory in txignore will be non-recursive, and child directories will not be ignored.


## Versioning
*Or, roxy how the fuck am i supposed to tell which of these is newest*

Like most of my themed projects, templ8 doesn't use semver, it uses some variant of it made by me. It is unnecessary and potentially cumbersome, but I like doing it. Here I explain it.

Define X, Y and Z as positive integers representing major release, minor release and patch, respectively. The specifics of what counts as each are completely arbitrary and decided by the project manager (me). Express a version following these rules:

- If Z = 0 and Y = 0, then write it as `8.X`.
- If Z = 0, then write it as `8.X.Y`.
- In any other case, write as `8.X.Y.Z`.
- `templ` might be appended before a version, for example: `templ8.5.3`
- If you want to do whatever specific thing not outlined here, do whatever, just keep it looking like it follows these rules.
  - Or not. I'm not a cop. `π` is the best templ8 version.
