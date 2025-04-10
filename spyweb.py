import subprocess

def run_subfinder(domain):
    try:
        # Run subfinder and capture the output
        result = subprocess.run(["subfinder", "-d", domain], capture_output=True, text=True)
        
        if result.returncode == 0:
            subdomains = result.stdout.strip().split("\n")
            
            # Save the results to a file
            with open(f"{domain}_subdomains.txt", "w") as f:
                f.write("\n".join(subdomains))
            
            print(f"Subdomains saved to {domain}_subdomains.txt")
            return subdomains
        else:
            print("Error running subfinder:", result.stderr)
            return []
    except FileNotFoundError:
        print("Error: subfinder is not installed or not in PATH.")
        return []

def check_sql_injection(url):
    try:
        # Run sqlmap with a simple test for SQL injection
        result = subprocess.run([
            "sqlmap", "--url", url, "--batch", "--level", "1", "--risk", "1"
        ], capture_output=True, text=True)
        
        if "is vulnerable" in result.stdout.lower():
            print(f"Potential SQL Injection vulnerability found: {url}")
            with open("vulnerable_subdomains.txt", "a") as f:
                f.write(url + "\n")
        else:
            print(f"No SQL injection found on {url}")
    except FileNotFoundError:
        print("Error: sqlmap is not installed or not in PATH.")

if __name__ == "__main__":
    domain = input("Enter the domain: ")
    subdomains = run_subfinder(domain)
    
    for subdomain in subdomains:
        url = f"http://{subdomain}"
        print(f"Checking: {url}")
        check_sql_injection(url)
