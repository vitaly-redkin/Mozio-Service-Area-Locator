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
