---
theme: gaia
transition: fade
style: |
  /* ⬇️ Mark the image of "1" in every pages as morphable image named as "one" ⬇️ */
  img[alt="1"] {
    view-transition-name: one;
    contain: layout; /* required */
  }

  /* Generic image styling for number icons */
  img:is([alt="1"], [alt="2"], [alt="3"]) {
    height: 64px;
    position: relative;
    top: -0.1em;
    vertical-align: middle;
    width: 64px;
  }
---

# Today's topics

- ![1](https://icongr.am/material/numeric-1-circle.svg?color=666666) Introduction
- ![2](https://icongr.am/material/numeric-2-circle.svg?color=666666) Features
- ![3](https://icongr.am/material/numeric-3-circle.svg?color=666666) Conclusion

---

<!-- _class: lead -->

![1 w:256 h:256](https://icongr.am/material/numeric-1-circle.svg?color=ff9900)

# Introduction

---

# ![1](https://icongr.am/material/numeric-1-circle.svg?color=666666) Introduction

Marp is an open-sourced Markdown presentation ecosystem.

It provides a writing experience of presentation slides by Markdown.