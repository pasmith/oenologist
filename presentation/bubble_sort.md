---
header: Bubble sort
transition: fade
style: |
  /* Define the style of "morph" class */
  .morph {
    display: inline-block;
    view-transition-name: var(--morph-name);
    contain: layout;
    vertical-align: top;
  }

  /* Global style */
  section {
    font-size: 60px;
  }
---

<span class="morph" style="--morph-name:b7;">███████</span> 7
<span class="morph" style="--morph-name:b5;">█████</span> 5
<span class="morph" style="--morph-name:b3;">███</span> 3
<span class="morph" style="--morph-name:b9;">█████████</span> 9

---

<span class="morph" style="--morph-name:b5;">█████</span> 5
<span class="morph" style="--morph-name:b7;">███████</span> 7
<span class="morph" style="--morph-name:b3;">███</span> 3
<span class="morph" style="--morph-name:b9;">█████████</span> 9

---

<span class="morph" style="--morph-name:b5;">█████</span> 5
<span class="morph" style="--morph-name:b3;">███</span> 3
<span class="morph" style="--morph-name:b7;">███████</span> 7
<span class="morph" style="--morph-name:b9;">█████████</span> 9

---

<span class="morph" style="--morph-name:b3;">███</span> 3
<span class="morph" style="--morph-name:b5;">█████</span> 5
<span class="morph" style="--morph-name:b7;">███████</span> 7
<span class="morph" style="--morph-name:b9;">█████████</span> 9