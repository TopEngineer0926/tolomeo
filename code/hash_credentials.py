from app.services.authentication.hmac import HmacAuth

# U = "set_here_your_username"
# P = "set_here_your_password"
U = "test@email.com"
P = "testpassword"

if __name__ == "__main__":
    print("Username: {}".format(HmacAuth().hexdigest_message(U)))
    print("Password: {}".format(HmacAuth().hexdigest_message(P)))
