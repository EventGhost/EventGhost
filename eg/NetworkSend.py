import socket
import md5
import locale

gEncoding = locale.getdefaultlocale()[1]


def NetworkSend(host, port, password, eventString, payload=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(2.0)
    connected = False
    try:
        sock.connect((host, port))
        connected = True
        sock.settimeout(1.0)
        # First wake up the server, for security reasons it does not
        # respond by it self it needs this string, why this odd word ?
        # well if someone is scanning ports "connect" would be very 
        # obvious this one you'd never guess :-) 

        sock.sendall("quintessence\n\r")

        # The server now returns a cookie, the protocol works like the
        # APOP protocol. The server gives you a cookie you add :<password>
        # calculate the md5 digest out of this and send it back
        # if the digests match you are in.
        # We do this so that none can listen in on our password exchange
        # much safer then plain text.

        cookie = sock.recv(128)        

        # Trim all enters and whitespaces off
        cookie = cookie.strip()

        # Combine the token <cookie>:<password>
        token = cookie + ":" + password

        # Calculate the digest
        digest = md5.new(token).hexdigest()

        # add the enters
        digest = digest + "\n"
                
        # Send it to the server        
        sock.sendall(digest)

        # Get the answer
        answer = sock.recv(512)

        # If the password was correct and you are allowed to connect
        # to the server, you'll get "accept"
        if (answer.strip() != "accept"):
            raise Exception("Server didn't send 'accept'")

        # now just pipe those commands to the server
        if (payload is not None) and (len(payload) > 0):
            for pld in payload:
                sock.sendall("payload " + pld.encode(gEncoding) + "\n")

        # send the eventstring
        sock.sendall(eventString.encode(gEncoding) + "\n")
        
        # tell the server that we are done nicely.
        sock.sendall("close\n")
        
    #except:
    #    return False
    finally:
        sock.close()
    
    return True


def Main(argv):
    host, port = argv[0].split(":")
    password = argv[1]
    eventstring = argv[2]
    payloads = argv[3:]
    NetworkSend(host, int(port), password, eventstring, payloads)
    
    
if __name__ == '__main__':
    import sys
    Main(sys.argv[1:])
