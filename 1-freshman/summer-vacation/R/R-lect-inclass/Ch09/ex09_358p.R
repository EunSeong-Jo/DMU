library(ggmap)
library(ggplot2)
register_google('AIzaSy...YHh8')

setwd('d:/source')
ds <- read.csv('시군구별_인구수_20222.csv')
ds$tot <- ds$Male + ds$Female

gc <- geocode(enc2utf8(ds$Region))
cen <- colMeans(gc, na.rm=T)
df <- data.frame(region=ds$Region, population=ds$tot,
                 lon=gc$lon, lat=gc$lat)
head(df)

map <- get_googlemap(center=cen,
                     map_type='roadmap',
                     zoom=8,
                     size=c(640,640))
gmap <- ggmap(map)
gmap+geom_point(data=df, 
                aes(x=lon, y=lat, size=population),
                alpha=0.5,
                col='red') +
  scale_size_continuous(range=c(1,12))