
# The Types of Presidental Documents

**Scope:** Describe the documents that are classified as *presidental* in the federal register

**Documents -> Presidential Documents -> Executive Orders**

*The structure of inheritance*

---
## Types of Presidental Documents

- Executive Orders
- Proclamation
- Memorandums
- Presidential Order
- Determination
- Notice
- Other

**The most common presidential documents are executive orders and proclamations**

---

## Executive Orders

We are probably most familiar with the Executive Order from history classes, this is no different; however we are parsing the JSON file that is associated with a paticular order. Understanding that, and the structure of the classes, in which Presidental Documents is a child class of Documents; means that we have to decide which fields are reserved for Executive Orders only, which is itself a child class of Presidental Documents.

| Element | Field Name | type | Inherited |
|:---|:---:|:---:|:---:|
| Abstract | abstract | str | yes |
| Action | action | str | yes |
| Agency | agency | List[Agency] | yes | 
| Document ID | doc_id | int | yes |
| 
