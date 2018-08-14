This is Mozio Service Area Python/Django Test Task.

The REST API has 5 end points and returns JSON data (save for the DELETE operations)

1. /providers/
- GET returns the list of all providers
- POST with JSON payload like 
<pre>
{
  "name": "Provider 1",
  "email": "test@test.com",
  "phone": "111",
  "currency": "USD",
  "language": "English"
}
</pre>            
creates a new provider

2. /providers/:provider_id/
- GET returns JSON with provider details (same as above but including ID)
- PUT with JSON payload like 
<pre>
{
  "name": "Provider 1",
  "email": "test@test.com",
  "phone": "111",
  "currency": "USD",
  "language": "English"
}
</pre>            
updates all provider fields
- PATCH with JSON payload like 
<pre>
{
  "phone": "222",
}
</pre>            
updates some provider fields
- DELETE removes the provider

3. /providers/:provider_id/serviceareas/
- GET returns the list of all service areas for the given provider
- POST with JSON payload like 
<pre>
{
  "name": "Area 1",
  "price": 123.45,
  "polygon": "{ \"type\": \"Polygon\", \"coordinates\": [ [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0] ] ] }"
}
</pre>            
creates a service area for the given provider. polygon here uses GeoJSON polygon format.

4. /providers/:provider_id/serviceareas/:service_area_id/
- GET returns JSON with service area details (same as above but including ID)
- PUT with JSON payload like 
<pre>
{
  "name": "Area 1",
  "price": 333.44,
  "polygon": "{ \"type\": \"Polygon\", \"coordinates\": [ [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0] ] ] }"
}
</pre>            
updates all service area fields
- PATCH with JSON payload like 
<pre>
{
  "price": 987.65,
}
</pre>            
updates some service area fields
- DELETE removes the service area
