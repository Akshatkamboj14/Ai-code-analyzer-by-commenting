provider "aws" {
  region = "us-east-1"
  shared_credentials_files = [ "~/.aws/credentials" ]
}

resource "aws_instance" "my-ec2" {
    ami = "ami-0a84ffe13366e143f"
    instance_type = "t2.micro"
    key_name = "akshatnv"


    tags = {
        name = "akshat-terraform"
    }
}


