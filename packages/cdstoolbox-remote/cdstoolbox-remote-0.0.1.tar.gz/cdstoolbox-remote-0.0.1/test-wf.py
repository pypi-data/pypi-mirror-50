import cdstoolbox as ct

@ct.application(title='Hello World!')
@ct.output.figure()
def application():

    data = ct.catalogue.retrieve(
        'seasonal-monthly-single-levels',
        {
            'originating_centre': 'ecmwf',
            'variable': '2m_temperature',
            'product_type': 'ensemble_mean',
            'year': '2018',
            'month': ['02'],
            'leadtime_month': ['1'],
            'format': 'grib'
        }
    )
    print(data)

    fig = ct.cdsplot.figure(subplot_kw={'projection': ct.cdsplot.crs.Robinson()})
    ct.cdsplot.geomap(
        data, pcolormesh_kwargs={'cmap': 'RdBu_r'}, fig=fig,
        title='Mean {long_name}'
    )

    return fig, data
