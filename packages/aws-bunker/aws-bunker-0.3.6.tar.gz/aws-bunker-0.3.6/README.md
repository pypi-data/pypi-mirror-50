# bunker  
  
Bunker is a command line program for setting up an ec2 in AWS for remote development or as a backup. Among other things, it can clone your git repos and transfer ignored files from your machine to the ec2.
  
## requirements  
  
- python  
- aws cli  
- boto3  
  
Also, you will need an EC2 instance on AWS, preferably running ubuntu>=18.04. This EC2 will need ssh (port 22) open and an attached SSM role (AmazonEC2RoleforSSM).  
   
## installation  
   
`$ pip intall aws-bunker`  
  
NOTE: see shell scripts, and terraform sections below:  
PROJECT HOME PAGE: https://gitlab.com/shindagger/bunker  
  
### shell scripts  
  
the `install` and `prompt` subcommands assume there will be shell scripts on the EC2 called. The default names (without positional arguments) are: `install-essentials.sh`, and `.prompt.sh` respectively.  
  
the first shell script is intended for essential software (like python, pip, node, and npm). If the script is not already executable, use the \[-e\] flag. `prompt` simply sources a file in ~/.profile on the EC2.  
  
See example scripts here (https://gitlab.com/shindagger/bunker) as well as the terraform section below:   
  
### terraform  
  
We have also included terraform files (https://gitlab.com/shindagger/bunker) which, when configured will spin up an EC2 instance you can use for bunker, with all the example shell scripts and your `.vimrc` provisioned. Of course you're encouraged to change these files according to preference. Terraform will output an instance ID you can use to init bunker with.  
  
To configure and use these terraform files:  
  
1. Clone this repo (https://gitlab.com/shindagger/bunker.git)  
  
2. cd into the repo dir and `ls *.default`. These are the files you will need to edit before you init terraform. Each one of these files will need the extension `.tf.default` changed to `.tf`.  
  
3. Edit `alfa.tf` and ensure that the region is correct.  
  
4. Edit `beta.tf` and change the s3 bucket to a bucket you own. Also ensure the region is correct.  
  
5. Edit `terraform.tfvars` with your AWS SDK access id and key. Also make sure you are configured to this account with `aws configure`  
  
6. Edit `variables.tf` and change the default values to reflect your wishes. NOTE: if you don't have them already, you will need to create your own ssm role, and ssh key file manually. `ec2_key_name` is just the name of the keypair in AWS, while `ssh_private_key` is the full (absolute) path to your .pem file on your local machine.  
  
7. `terraform init`  
  
8. `terraform plan && terraform apply`  
  
### before you init bunker  
  
1. You have an EC2 instance ID. (see "terraform" above)  
  
2. You have a directory (prefix) in which you will keep `repositories.txt` and `ignoredfiles.txt`. You can copy sample files from this repo, and edit them to reflect your repos and ignored files.  
  
3. You have a .pem file and you know the path to its location. You have a keypair name set for your EC2, which uses this .pem file.  
  
4. You know the username for the EC2 \(should be "ubuntu"\). We may choose to support other OSs in future versions.    
  
5. You have created a private key for your git provider, and you added the public key in your git provider settings. Also, you have configured your local ssh to use this key and tested or used it at least once.  
  
## bunker usage  
  
`$ bunker -h`  
  
**Show main bunker help page and exit**  
  
`$ bunker build -h`  
  
**Show help page for the subcommand `build` and exit.** This will work with any available subcommand  
  
`$ bunker init`  
  
**Write the bunker config file `~/.config-bunker.ini`.** If the file exists already, answers will be populated with existing values \[underlined\], and only overwritten if you offer a replacement value.  
  
example `~/.config-bunker.ini`:
```
[default]  
prefix = /Users/username/bunker-config  
repos = repositories.txt   
ignored = ignoredfiles.txt  
pem = /Users/username/somename.pem  
instance_id = i-04xxxxxxxxxxxx148  
username = ubuntu  
gitkeys = /Users/username/.ssh/git_rsa  
```  
  
`$ bunker repo path/to/repo /absolute/path/to/another-repo ../somerepo`   
   
**Add or remove repo directories to/from repo file.** Use relative or absolute paths.  
   
`$ bunker ignore .env.local config.ini terraform.tfvars`  
  
**Add or remove filenames to/from ignore file.**   
  
`$ bunker install`  
`$ bunker install /home/ubuntu/script.sh`  
   
**Install essential software on your EC2 instance.** This command will run an executable shell script on your EC2. The default script (without defining the positional argument) is named `/home/ubuntu/install-essentials.sh`. This is intended to install any software essential to using your EC2. In an effort to stay agnostic about what software users want on their EC2, bunker does not install with included shell scripts. We do however provide example shell scripts \(as well as terraform for the EC2\) at the project homepage:   
https://gitlab.com/shindagger/bunker  
  
`$ bunker prompt`  
`$ bunker prompt /home/ubuntu/another-prompt.sh`  
   
**Source a custom prompt file in `/home/ubuntu/.profile`.** This command will source a file in `/home/ubuntu/.profile`. The default name is: `/home/ubuntu/.prompt.sh`.    
  
`$ bunker build`  
  
**Clone list of git repos \(repositories.txt\) on your EC2 and then rsync list of ignored files \(ignoredfiles.txt\) from your local repos to the EC2 repos.** `git clone` will use ssh, assuming you have a public key setup at your git provider, a working `~/.ssh/config` tested at least once with `ssh -T git@PROVIDERURL`, and the associated private key set using `bunker init`.  
  
