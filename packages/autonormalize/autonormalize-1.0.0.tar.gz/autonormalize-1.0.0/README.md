# AutoNormalize

[![CircleCI](https://circleci.com/gh/FeatureLabs/autonormalize.svg?style=shield&circle-token=b890443ca669d7e88d62ad2fd712f92951550c4a)](https://circleci.com/gh/FeatureLabs/autonormalize)

AutoNormalize is a Python library for automated datatable normalization, intended for use with [Featuretools](https://github.com/Featuretools/featuretools). AutoNormalize allows you to build an `EntitySet` from a single denormalized table and generate features for machine learning.

![](gif.gif)

### Install
```shell
pip install featuretools[autonormalize]
```
### Uninstall
```shell
pip uninstall autonormalize
```
<br />

### API Reference

#### `auto_entityset`
```shell
auto_entityset(df, accuracy=0.98, index=None, name=None, time_index=None)
```
Creates a normalized entityset from a dataframe.

**Arguments:**

* `df` (pd.Dataframe) : the dataframe containing data

* `accuracy` (0 < float <= 1.00; default = 0.98) : the accuracy threshold required in order to conclude a dependency (i.e. with accuracy = 0.98, 0.98 of the rows must hold true the dependency LHS --> RHS)

* `index` (str, optional) : name of column that is intended index of df

* `name` (str, optional) : the name of created EntitySet

* `time_index` (str, optional) : name of time column in the dataframe.

**Returns:**

* `entityset` (ft.EntitySet) : created entity set

<br />

#### `find_dependencies`

```shell
find_dependencies(df, accuracy=0.98, index=None)
```
Finds dependencies within dataframe with the DFD search algorithm.

**Returns:**

*  `dependencies` (Dependencies) : the dependencies found in the data within the contraints provided

<br />

#### `normalize_dataframe`

```shell
normalize_dataframe(df, dependencies)
```
Normalizes dataframe based on the dependencies given. Keys for the newly created DataFrames can only be columns that are strings, ints, or categories. Keys are chosen according to the priority: 
1) shortest lenghts 
2) has "id" in some form in the name of an attribute 
3) has attribute furthest to left in the table

**Returns:**

* `new_dfs` (list[pd.DataFrame]) : list of new dataframes

<br />

#### `make_entityset`

```shell
make_entityset(df, dependencies, name=None, time_index=None)
```
Creates a normalized EntitySet from dataframe based on the dependencies given. Keys are chosen in the same fashion as for `normalize_dataframe`and a new index will be created if any key has more than a single attribute.

**Returns:**

* `entityset` (ft.EntitySet) : created EntitySet

<br />

#### `normalize_entity`

```shell
normalize_entity(es, accuracy=0.98)
```
Returns a new normalized `EntitySet` from an `EntitySet` with a single entity.

**Arguments:**

* `es` (ft.EntitySet) : EntitySet with a single entity to normalize

**Returns:**

* `new_es` (ft.EntitySet) : new normalized EntitySet

<br />

## Feature Labs
<a href="https://www.featurelabs.com/">
    <img src="http://www.featurelabs.com/wp-content/uploads/2017/12/logo.png" alt="Featuretools" />
</a>

AutoNormalize is an open source project created by [Feature Labs](https://www.featurelabs.com/). To see the other open source projects we're working on visit Feature Labs [Open Source](https://www.featurelabs.com/open). If building impactful data science pipelines is important to you or your business, please [get in touch](https://www.featurelabs.com/contact/).
