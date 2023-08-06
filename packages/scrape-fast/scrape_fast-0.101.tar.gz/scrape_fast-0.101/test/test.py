
import scrape_fast

r = scrape_fast.simple.make_request('http://www.google.com')
print(r.status_code)