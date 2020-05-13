def columns(x):
    return len(list(x.columns))

def rows(x):
    return len(list(x.T.columns))

def per_c_miss_info(x):
    return (len(list(x.columns))/x.isnull().sum().count())*100

def per_r_miss_info(x):
    return (len(list(x.T.columns))/x.T.isnull().sum().count())*100

def col_miss_95(x):
    return list(x.isnull().sum()[x.isnull().sum() > (rows(x)*0.95) ].index)

def row_miss_95(x):
    return list(x.T.isnull().sum()[x.T.isnull().sum() > (columns(x)*0.95) ].index)

def print_shape(x):
    return print(f"""The df has {x.shape} (rows/colums)
Rows: {rows(x)}
Coulms: {columns(x)}
    {x.columns}""")