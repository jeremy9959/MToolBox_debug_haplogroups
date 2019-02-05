# MToolBox_debug_haplogroups

The notebook is tested in python2.

## New rules for NoLabel nomenclature

### Case 1

If a branch is a NoLabel, inherits the parent name, to which a list of mutations separated by `_` is appended. Eg:

```
A2
|-- A2a, mutations: 100, 150, 200
|-- NoLabel, mutations: 120, 130
```

The NoLabel in the example becomes `A2_120_130`.

### Case 2

Some NoLabels have only unstable mutations (annotated between brackets in Phylotree). Since in this case there is no mutation to be appended, a `\_s<int>` will be appended, where `<int>` is a serial number. This serial number is used to avoid confusion in case there are two NoLabels with only unstable mutations which are children of the same parent. Eg:

```
A3
|-- A3a, mutations: 100, 150, 200
|-- NoLabel, mutations: (120)
|-- NoLabel, mutations: (200)
```

The two NoLabels will become `A3_s1` and `A3_s2`, respectively.

### Some remarks

In the script which assigns the names to the haplogroups, the `<int>` appended to the haplogroups in case 2 is merely based on the order of appearance of such haplogroups in the tree parsing. Therefore, parsing future releases of the mt phylogeny could change the value of `<int>`. Haplogroups in case 2, therefore, should be reported with the specific phylotree release, _eg_ **A3_s1 (p17)**. However, while I'm writing this, I think that no genome will ever be assigned to such haplogroups, since they have no mutations which could specifically lead to them. So the above mentioned recommendations are still good, but anyway LOL.  

A major consideration is about the haplogroup assignment system. Basically, A3_s1 and A3 will be defined by the same mutations, since A3_s1 has no additional mutation compared to A3, so a sequence assigned to A3 should be assigned to A3_s1 as well. Since this makes no sense, we should add a check in the haplogroup assignment: when the best haplogroups assignments include these nodes, they should be discarded (ie, check if `_s` is in the haplogroup name).