# HHInjector
Simple Tool to check Host Header Injection Vulnerability

To use the tool you only have to:

1. Clone this repository
   
   git clone https://github.com/esquilichi/HHInjector/
   
2. Install dependencies with pip/pip3

   pip3 install -r requirements.txt
   
   
 3. Use main.py 
    
    python3 main.py -l comma_separated_links.txt
    python3 main.oy -u http(s)://url_to_test
    
    
    
    
VERY IMPORTANT

Sometimes servers behave in one way or another depending if you make the http request or https.
I recommend to make a list of all domains you want to test with both protocols.

!Happy Hacking!
