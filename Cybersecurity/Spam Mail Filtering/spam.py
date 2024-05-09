def spam_filter(email_text):
    spam_keywords=['offer','discount','free','prize','limited','money','order']
    spam_count=sum(email_text.lower().count(keyword) for keyword in spam_keywords)
    spam_threshold=3

    if spam_count>=spam_threshold:
        return True
    else:
        return False
    
if __name__=="__main__":
        email=str(input("Enter email :"))

if spam_filter(email):
        print("Email is spam.")
else:
     print("Email is not spam.")
    
    