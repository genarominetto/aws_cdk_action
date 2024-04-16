ln -sf /usr/bin/python3 /usr/bin/python
ln -sf /usr/bin/pip3 /usr/bin/pip

apk add py3-pip

pip install --upgrade pip --break-system-packages
pip install somepackage --break-system-packages

# Install aws-cdk-lib and constructs which include all necessary AWS services
pip install aws-cdk-lib constructs --break-system-packages

# Assuming that the project is already correctly initialized and requirements.txt is at the root
pip install -r requirements.txt --break-system-packages

aws --profile default configure set region "us-east-1"
aws --profile default configure set output "json"

cdk synth
cdk deploy

