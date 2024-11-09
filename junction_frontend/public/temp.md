## Writing template strings in Markdown

With template strings coming to ES6, the backtick (`` ` ``) means something in Markdown and in JavaScript. If you write this:

    To display a message, write `alert(`hello world!`)`.

it'll render like this:

> To display a message, write `alert(`hello world!`)`.

So how can you mix ES6 template strings with Markdown?


### Use double backticks

Markdown has always supported using **multiple backticks** as code delimiters. If you use two, or three, or four backticks to start a snippet of code, then any *shorter* sequences of backticks within that snippet are shown verbatim in the output.

For example, if you want the output to look like this:  ``alert(`${color} alert!`)``

just type: ``` ``alert(`${color} alert!`)`` ```

(In order to make the previous line look like that, I had to use triple-backticks. [View source.](https://gist.githubusercontent.com/jorendorff/6532f6d1a3e21bbf643c/raw/8912af9eb526b030d023e7ce2b60ec6a5e5a074a/gfm.md))


### Fenced code blocks are fine

In Github Flavored Markdown [fenced code blocks](https://help.github.com/articles/github-flavored-markdown/#fenced-code-blocks), you don't have to do anything special at all. Template strings don't cause any problems there, though Github's syntax highlighting library doesn't seem to recognize them yet.

This Markdown:

    ```javascript
    var headline = `${greetings}, ${location}${enthusiasm_level}`;
    $("#post").html`
      <h1>${headline}</h1>
      ${body}
    `;
    ```

looks like this:

```javascript
var headline = `${greetings}, ${location}${enthusiasm_level}`;
$("#post").html`
  <h1>${headline}</h1>
  ${body}
`;
```