---
marp: true
theme: uncover
class: invert
math: katex
style: |
  .columns {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
  }
transition: fade
---

# An intro to Marp :rocket:
<span style="color:grey">By:</span> Patrick Smith

---

## Slide Header

* Use Markdown to write slides!
* Tons of cool features!

---

## Bullets!

- 1
- 2
- 3

---

## Code!

``` python
def fibonacci():
  a, b = 0,1
  while True:
    yield a
    a, b = b, a + b

```

---

## Math!

$\mathcal{O}(nlog{n})$

---

## Images


---

## Two Columns!

![bg left height:4in]()

* a
* b

---

<!--_color: red-->
<!--_backgroundColor: black-->
# <!--fit-->Huge


---

## Two text columns!

<div class="columns">
  <div>

  * a
  * b
  * c

  </div>
  <div>

  1. d
  1. e
  1. f

  </div>
</div>

---

