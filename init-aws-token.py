import pyperclip
import os

text = pyperclip.paste()
f = open("token.txt", 'w')
f.write(text)
f.close()
f = open("token.txt",'rb+')
byte = f.readlines()
print(byte)
key_id = byte[1].decode("utf-8")[18:]
print("get the key_is is " + key_id)
access_key = byte[2].decode("utf-8")[22:]
print("get the access_key is " + access_key)
token = byte[3].decode("utf-8")[18:]
print("get the token is " + token)
os.system("rm -fr ~/.aws/credentials")
os.system("touch ~/.aws/credentials")
f = open("/Users/taoli/.aws/credentials", 'w')
f.write("[default]\n")
f.write("aws_access_key_id = " + key_id)
f.write("aws_secret_access_key = " + access_key)
f.write("aws_session_token = " + token)
f = open("/Users/taoli/.aws/credentials",'rb+')
config_content = f.readlines()
print("the config content first line:   " + config_content[0].decode("utf-8"))
print("the config content second line:   " + config_content[1].decode("utf-8"))
print("the config content third line:   " + config_content[2].decode("utf-8"))
print("the config content four line:   " + config_content[3].decode("utf-8"))
os.system("aws eks update-kubeconfig --region ap-southeast-1 --name taoli-cluster")
os.system("export KUBECONFIG=$KUBECONFIG:~/.kube/config")