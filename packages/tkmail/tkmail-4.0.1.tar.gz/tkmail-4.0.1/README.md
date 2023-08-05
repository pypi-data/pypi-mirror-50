### Simple Usage

```python
from tkmail import Email

email = Email(
  host='smtp.gmail.com', 
  port=587, 
  use_tls=True,
  username='demo@gmail.com',
  password='hidden_password',
  to='anonymous@gmail.com',
  cc='somebody@gmail.com',
  bcc='another@gmail.com',
  subject='Demo sending email',
).html('<h1>Demo sending email</h1>').send().retry(times=5)
```