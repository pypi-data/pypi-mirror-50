# istSOS𝜇 protocol buffer repository.

This module contains all the proto files of istsos.

## Qry Utils

## Simple usage example

```python

from istsosproto import qry

conditions = qry(
    {
        "value": "value_obs",
        "updated": "updated_obs"
    }
).get_conditions(
    Where(
        operator=Where.AND,
        where=[
            Where(
                operator=Where.GREATER_THAN,
                property='value',
                measure=2.0
            ),
            Where(
                operator=Where.NOT_NULL,
                property='updated'
            )
        ]
    )
)

print(conditions)

```

*get_conditions* call returns a tuple with the SQL and a list of parameters: 

```python
('(value_obs > $1 AND updated_obs IS NOT NULL)', [2.0])
```

## Comparison operators

Supported operators:

- NULL
- NOT_NULL
- EQUALS
- NOT_EQUALS
- LIKE
- GREATER_THAN
- GREATER_THAN_OR_EQUAL_TO
- LESS_THAN
- LESS_THAN_OR_EQUAL_TO

### NULL

```python
Where(
    operator=Where.NULL,
    property='updated'
)
```
result:

```python
(
    "updated IS NULL",
    []
)
```

### NOT_NULL

```python
Where(
    operator=Where.EQUALS,
    property='updated'
)
```
result:

```python
(
    "updated IS NOT NULL",
    []
)
```

### EQUALS

```python
Where(
    operator=Where.EQUALS,
    property='value',
    mesaure=10.9
)
```
result:

```python
(
    "value = $1",
    [10.9]
)
```

### NOT_EQUALS

```python
Where(
    operator=Where.NOT_EQUALS,
    property='value',
    mesaure=10.9
)
```
result:

```python
(
    "value <> $1",
    [10.9]
)
```

### LIKE

```python
Where(
    operator=Where.LIKE,
    property='name',
    text='%foo'
)
```
result:

```python
(
    "name IS LIKE $1",
    ['%foo]
)
```

## Usage with function

Supported functions are:

- STARTS_WITH
- ST_INTERSECTS
- ST_DWITHIN
- ST_CONTAINS


### INTERSECTS

```python

from qry import *

conditions = qry(
    {
        "geom": "geom_loc"
    }
).get_conditions(
    Where(
        function=Where.ST_INTERSECTS,
        property='geom',
        ewkt='SRID=4326;BOX(-180 -90, 180 90)'
    )
)

print(conditions)

```
*get_conditions* call returns a tuple with the SQL and a list of parameters: 

```python
(
    "ST_Intersects(geom_loc, ST_GeomFromEWKT($1))",
    ['SRID=4326;BOX(-180 -90, 180 90)']
)
```

### DWITHIN

```python

from qry import *

conditions = qry(
    {
        "geom": "geom_loc"
    }
).get_conditions(
    Where(
        function=Where.ST_DWITHIN,
        property='geom',
        ewkt='SRID=3857;POINT(3072163.4 7159374.1)',
        xmeasure=200
    )
)

print(conditions)

```

*get_conditions* call returns a tuple with the SQL and a list of parameters: 

```python
(
    "ST_DWithin(geom_loc, ST_GeomFromEWKT($1), $2)",
    ['SRID=4326;BOX(-180 -90, 180 90)', 200]
)
```

### CONTAINS

```python

from qry import *

conditions = qry(
    {
        "geom": "geom_loc"
    }
).get_conditions(
    Where(
        function=Where.ST_CONTAINS,
        property='geom',
        ewkt='SRID=3857;POINT(3072163.4 7159374.1)',
        xmeasure=200
    )
)

print(conditions)

```

*get_conditions* call returns a tuple with the SQL and a list of parameters: 

```python
(
    "ST_Contains(geom_loc, ST_GeomFromEWKT($1))",
    ['SRID=3857;POINT(3072163.4 7159374.1)']
)
```
