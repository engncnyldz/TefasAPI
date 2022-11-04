# TefasAPI

This is a Python application which is used to create an HTTP endpoint that retrieves fund prices shared by Tefas (Türkiye Elektronik Fon Alım Satım Platformu), https://www.tefas.gov.tr/Hakkinda.aspx <br />
It queries fund search page (https://www.tefas.gov.tr/FonAnaliz.aspx?), extracts main data and serves them under `hostname:port/funds/{code}` <br />

It caches fund data using Redis, since fund prices do not get updated momentarily. <br />
The application requires following environment variables:

`REDIS_HOST`: Redis client hostname.  <br />
`REDIS_PORT`: Redis client port.  <br />
`REFRESH_HOUR`: An integer that indicates at which hour during the day the data will be refreshed (0-23)
