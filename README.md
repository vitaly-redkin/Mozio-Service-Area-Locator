This is Mozio Service Area Python/Django Test Task.

The REST API has 5 end points and returns JSON data (save for the DELETE operations)

1. /providers/
- GET
Returns the list of all providers
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
