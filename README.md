# brute-ng🚀
Hey there! Welcome to my little project. A Python script designed to handle a common challenge in web security: dealing with dynamic CSRF (Cross-Site Request Forgery) tokens during password brute-forcing processes. 

# Features
## Usage of ThreadPoolExecutor:
- **Purpose:** The ThreadPoolExecutor is used for handling multiple login attempts concurrently.
- **Advantage:** The script mainly involves I/O-bound operations, primarily waiting for network responses. ThreadPoolExecutor excels in such scenarios by enabling multiple HTTP requests to be made in parallel, effectively overcoming the I/O bottleneck. This is in contrast to multiprocessing, which is more suited for CPU-bound tasks where processing power is the limiting factor.
## Automated Session Handling:
- The script initially performs a GET request to fetch the session cookie (PHPSESSID). This cookie is crucial for maintaining the session state during subsequent requests.
## Automated CSRF Tokens Handling:
- The script deals with this by retrieving a new CSRF token for each login attempt, ensuring that each request is valid and adheres to the security protocols of the target website.

# How to Use It
```bash
python brute.py -w [wordlist]
```
# To-Do
1. [ ] Add more custom options e.g. number of concurrent workers, custom username wordlist.
2. [ ] Fix thread pool clean-up after finding a valid password.
3. [ ] Optimized thread pool job submission and memory when dealing with large wordlist.

# A Friendly Heads-Up!
This script is for learning and legal security testing. If you're using it, you're responsible for your actions.
