$body = @{lat=18.7883; lng=98.9853; distance=5.0; pace='5:45'; steps=5200} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:3000/api/runs/ai-summary" -Method Post -ContentType "application/json" -Body $body
