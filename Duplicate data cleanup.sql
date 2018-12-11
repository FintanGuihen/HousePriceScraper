USE [TestDatabase]
GO


use testdatabase
go

CREATE TABLE [dbo].[MyHome3](
	[PropertyAddress] [varchar](500) NULL,
	[beds] [varchar](50) NULL,
	[baths] [varchar](50) NULL,
	[ber] [varchar](50) NULL,
	[size] [varchar](50) NULL,
	[propertyType] [varchar](50) NULL,
	[price] [varchar](150) NULL,
	[agent] [varchar](1050) NULL,
	[increase] [varchar](50) NULL,
	[decrease] [varchar](50) NULL,
	[webpage] [varchar](500) NULL,
	[propertyURL] [varchar](500) NULL
) ON [PRIMARY]

GO

--backup the original data
select * into [MyHome3_Backup]
from [MyHome3]


select count(*) from myHome3
where 
select count(*) from [MyHome3_Backup]

alter table myhome3
add Duplicate bit


--get the location category
update myhome3
set LocationCategory = reverse(SUBSTRING(reverse(webpage),CHARINDEX('/',reverse(webpage))+1, CHARINDEX('/',reverse(webpage),CHARINDEX('/',reverse(webpage))+1) -CHARINDEX('/',reverse(webpage))-1)) 
from MyHome3

--get distinct list of location categories used on the site
select distinct locationCategory from myhome3 mh
join 
(
	select count(*) dupCount, propertyURL
	from myHome3
	group by propertyURL
	having count(*) >1
)as dup on mh.propertyURL = dup.propertyURL
order by mh.propertyURL


--find all properties that have a postcode, but are also in the "dublin" group all category, these ones in the groupall category are duplicates.

select mh.PropertyAddress, mh.propertyURL, mh.webpage,mh.locationCategory, mh.duplicate, mh2.PropertyAddress, mh2.propertyURL, mh2.webpage, mh2.locationCategory, mh2.decrease
from myHome3 mh
 join myhome3 mh2 on mh.propertyURL = mh2.propertyURL
where mh.LocationCategory = 'dublin'
and mh2.LocationCategory in(
	'dublin-1'
	,'dublin-10'
	,'dublin-11'
	,'dublin-12'
	,'dublin-13'
	,'dublin-14'
	,'dublin-15'
	,'dublin-16'
	,'dublin-17'
	,'dublin-18'
	,'dublin-2'
	,'dublin-20'
	,'dublin-22'
	,'dublin-24'
	,'dublin-3'
	,'dublin-4'
	,'dublin-5'
	,'dublin-6'
	,'dublin-6w'
	,'dublin-7'
	,'dublin-8'
	,'dublin-9'
)

--flag properties in the general category "dublin" as duplicates
Begin Tran
update mh
set mh.duplicate = 1
from myHome3 mh
 join myhome3 mh2 on mh.propertyURL = mh2.propertyURL
where mh.LocationCategory = 'dublin'
and mh2.LocationCategory in(
	'dublin-1'
	,'dublin-10'
	,'dublin-11'
	,'dublin-12'
	,'dublin-13'
	,'dublin-14'
	,'dublin-15'
	,'dublin-16'
	,'dublin-17'
	,'dublin-18'
	,'dublin-2'
	,'dublin-20'
	,'dublin-22'
	,'dublin-24'
	,'dublin-3'
	,'dublin-4'
	,'dublin-5'
	,'dublin-6'
	,'dublin-6w'
	,'dublin-7'
	,'dublin-8'
	,'dublin-9'
)
--rollback
--commit


select mh.PropertyAddress, mh.propertyURL, mh.webpage,mh.locationCategory, mh.duplicate, mh2.PropertyAddress, mh2.propertyURL, mh2.webpage, mh2.locationCategory, mh2.decrease
from myHome3 mh
 join myhome3 mh2 on mh.propertyURL = mh2.propertyURL
where mh.LocationCategory = 'dublin'
and mh2.LocationCategory in(
	 'dublin-county'
	,'dublin-north'
	,'dublin-north-county'
	,'dublin-south'
	,'dublin-south-county'
	,'dublin-west'
)


update mh
set mh.duplicate = 1
from myHome3 mh
 join myhome3 mh2 on mh.propertyURL = mh2.propertyURL
where mh.LocationCategory = 'dublin'
and mh2.LocationCategory in(
	 'dublin-county'
	,'dublin-north'
	,'dublin-north-county'
	,'dublin-south'
	,'dublin-south-county'
	,'dublin-west'
)


select mh.PropertyAddress, mh.propertyURL, mh.webpage,mh.locationCategory, mh.duplicate, mh2.PropertyAddress, mh2.propertyURL, mh2.webpage, mh2.locationCategory, mh2.decrease
from myHome3 mh
 join myhome3 mh2 on mh.propertyURL = mh2.propertyURL
where mh.LocationCategory = 'dublin-county'
and mh2.LocationCategory in(
	'dublin-north'
	,'dublin-north-county'
	,'dublin-south'
	,'dublin-south-county'
	,'dublin-west'
)


update mh
set mh.duplicate = 1
from myHome3 mh
 join myhome3 mh2 on mh.propertyURL = mh2.propertyURL
where mh.LocationCategory = 'dublin-county'
and mh2.LocationCategory in(
	'dublin-north'
	,'dublin-north-county'
	,'dublin-south'
	,'dublin-south-county'
	,'dublin-west'
)


update mh
set mh.duplicate = 1
from myHome3 mh
 join myhome3 mh2 on mh.propertyURL = mh2.propertyURL
where mh.LocationCategory = 'dublin-north'
and mh2.LocationCategory in(
	'dublin-1'
	,'dublin-10'
	,'dublin-11'
	,'dublin-12'
	,'dublin-13'
	,'dublin-14'
	,'dublin-15'
	,'dublin-16'
	,'dublin-17'
	,'dublin-18'
	,'dublin-2'
	,'dublin-20'
	,'dublin-22'
	,'dublin-24'
	,'dublin-3'
	,'dublin-4'
	,'dublin-5'
	,'dublin-6'
	,'dublin-6w'
	,'dublin-7'
	,'dublin-8'
	,'dublin-9'
)


update mh
set mh.duplicate = 1
from myHome3 mh
 join myhome3 mh2 on mh.propertyURL = mh2.propertyURL
where mh.LocationCategory = 'dublin-north-county'
and mh2.LocationCategory in(
	'dublin-1'
	,'dublin-10'
	,'dublin-11'
	,'dublin-12'
	,'dublin-13'
	,'dublin-14'
	,'dublin-15'
	,'dublin-16'
	,'dublin-17'
	,'dublin-18'
	,'dublin-2'
	,'dublin-20'
	,'dublin-22'
	,'dublin-24'
	,'dublin-3'
	,'dublin-4'
	,'dublin-5'
	,'dublin-6'
	,'dublin-6w'
	,'dublin-7'
	,'dublin-8'
	,'dublin-9'
)


update mh
set mh.duplicate = 1
from myHome3 mh
 join myhome3 mh2 on mh.propertyURL = mh2.propertyURL
where mh.LocationCategory = 'dublin-south'
and mh2.LocationCategory in(
	'dublin-1'
	,'dublin-10'
	,'dublin-11'
	,'dublin-12'
	,'dublin-13'
	,'dublin-14'
	,'dublin-15'
	,'dublin-16'
	,'dublin-17'
	,'dublin-18'
	,'dublin-2'
	,'dublin-20'
	,'dublin-22'
	,'dublin-24'
	,'dublin-3'
	,'dublin-4'
	,'dublin-5'
	,'dublin-6'
	,'dublin-6w'
	,'dublin-7'
	,'dublin-8'
	,'dublin-9'
)

update mh
set mh.duplicate = 1
from myHome3 mh
 join myhome3 mh2 on mh.propertyURL = mh2.propertyURL
where mh.LocationCategory = 'dublin-south-county'
and mh2.LocationCategory in(
	'dublin-1'
	,'dublin-10'
	,'dublin-11'
	,'dublin-12'
	,'dublin-13'
	,'dublin-14'
	,'dublin-15'
	,'dublin-16'
	,'dublin-17'
	,'dublin-18'
	,'dublin-2'
	,'dublin-20'
	,'dublin-22'
	,'dublin-24'
	,'dublin-3'
	,'dublin-4'
	,'dublin-5'
	,'dublin-6'
	,'dublin-6w'
	,'dublin-7'
	,'dublin-8'
	,'dublin-9'
)

update mh
set mh.duplicate = 1
from myHome3 mh
 join myhome3 mh2 on mh.propertyURL = mh2.propertyURL
where mh.LocationCategory = 'dublin-west'
and mh2.LocationCategory in(
	'dublin-1'
	,'dublin-10'
	,'dublin-11'
	,'dublin-12'
	,'dublin-13'
	,'dublin-14'
	,'dublin-15'
	,'dublin-16'
	,'dublin-17'
	,'dublin-18'
	,'dublin-2'
	,'dublin-20'
	,'dublin-22'
	,'dublin-24'
	,'dublin-3'
	,'dublin-4'
	,'dublin-5'
	,'dublin-6'
	,'dublin-6w'
	,'dublin-7'
	,'dublin-8'
	,'dublin-9'
)





--*******************************CORK******************************************
select count(*), LocationCategory
from myHome3
where duplicate is null
and locationcategory like '%cork%'
group by LocationCategory
order by count(*) desc


select mh2.*
from myHome3 mh
left outer join myHome3 mh2 on mh.propertyurl = mh2.propertyURL
where mh.LocationCategory = 'cork-west'
and mh2.LocationCategory != 'cork-west'

update mh2
set mh2.duplicate = 1
from myHome3 mh
left outer join myHome3 mh2 on mh.propertyurl = mh2.propertyURL
where mh.LocationCategory = 'cork-west'
and mh2.LocationCategory != 'cork-west'
--********************************************
--599 records in cork category that are duplicates
--********************************************

select mh2.*
from myHome3 mh
left outer join myHome3 mh2 on mh.propertyurl = mh2.propertyURL
where mh.LocationCategory = 'cork-city'
and mh2.LocationCategory != 'cork-city'

update mh2
set mh2.duplicate = 1
from myHome3 mh
left outer join myHome3 mh2 on mh.propertyurl = mh2.propertyURL
where mh.LocationCategory = 'cork-city'
and mh2.LocationCategory != 'cork-city'

--********************************************
--414 records in cork category that are duplicates
--********************************************



select count(*), LocationCategory
from myhome3
group by 

select count(*) from myhome3
where duplicate is null




