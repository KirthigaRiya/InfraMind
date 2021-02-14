
import json
import boto3


def lambda_handler(event, context):
  print(event)
  data = json.loads(event['body'])
  print(data)
  
  template = {
        
        "AWSTemplateFormatVersion": "2010-09-09",
        "Description": "Template for ec2 instance",
        "Resources":{
          "VPC" :vpc(),
          "PublicSubnet1":PublicSubnet1(),
          "PublicSubnet2":PublicSubnet2(),
          "PrivateSubnet":PrivateSubnet(),
          "InternetGateway":InternetGateway(),
          "VpcGatewayAttachment":VpcGatewayAttachment(),
          "PublicSubnet1RouteTable":PublicSubnet1RouteTable(),
          "PublicSubnet1RouteTableSubnetAssociation":PublicSubnet1RouteTableSubnetAssociation(),
          "PublicSubnet1RouteTableRouteAssociation":PublicSubnet1RouteTableRouteAssociation(),
          "PublicSubnet2RouteTable":PublicSubnet2RouteTable(),
          "PublicSubnet2RouteTableSubnetAssociation":PublicSubnet2RouteTableSubnetAssociation(),
          "PublicSubnet2RouteTableRouteAssociation":PublicSubnet2RouteTableRouteAssociation(),
          "ElasticIP":ElasticIP(),
          "NATGateway":NATGateway(),
          "PrivateSubnetRouteTable":PrivateSubnetRouteTable(),
          "PrivateSubnetRouteTableSubnetAssociation":PrivateSubnetRouteTableSubnetAssociation(),
          "PrivateSubnetRouteTableRouteAssociation":PrivateSubnetRouteTableRouteAssociation(),
          "LoadBalancerSecurityGroup":LoadBalancerSecurityGroup(),
          "WordpressSecurityGroup":WordpressSecurityGroup(),
          "MySqlDbSecurityGroup":MySqlDbSecurityGroup(),
          "WordpressInstance":WordpressInstance(),
          "WordpressLoadBalancer":WordpressLoadBalancer(),
          "WordpressTargetGroup":WordpressTargetGroup(),
          "WordpressLoadBalancerListener":WordpressLoadBalancerListener(),
          "WordpressLaunchConfiguration":WordpressLaunchConfiguration(),
          "WordpressAutoScalingGroup":WordpressAutoScalingGroup(),
          "ScalingPolicy":ScalingPolicy(),
          "MySqlDbInstance":MySqlDbInstance()
           
           
        }
        
    }

  a = json.dumps(template)
    
  cf = boto3.client('cloudformation')
    
  try:
    response = cf.create_stack(StackName='test2', TemplateBody=a)
    print(response)
  except Exception as e:
    print(e)
    
  return  {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

  
  

def vpc():
    return {
      "Type": "AWS::EC2::VPC",
      "Properties": {
        "CidrBlock":"10.0.0.0/16",
        "Tags" :[ {"Key" : "Name", "Value" : "Vpc"} ]
      }
    }
    
def PublicSubnet1():
    return {
      "DependsOn": "VPC",
      "Type": "AWS::EC2::Subnet",
      "Properties": {
        "VpcId": {
          "Ref": "VPC"
        },
        "AvailabilityZone": "us-east-1a",
        "CidrBlock":"10.0.1.0/24",
        "Tags" :[ {"Key" : "Name", "Value" : "PublicSubnet1"} ]
      }
    }
    
def PublicSubnet2():
    return  {
      "DependsOn": "VPC",
      "Type": "AWS::EC2::Subnet",
      "Properties": {
        "VpcId": {
          "Ref": "VPC"
        },
        "AvailabilityZone": "us-east-1b",
        "CidrBlock":"10.0.2.0/24",
        "Tags" :[ {"Key" : "Name", "Value" : "PublicSubnet2"} ]
      }
    }
def  PrivateSubnet():
    return  {
      "DependsOn": "VPC",
      "Type": "AWS::EC2::Subnet",
      "Properties": {
        "VpcId": {
          "Ref": "VPC"
        },
        "AvailabilityZone": "us-east-1c",
        "CidrBlock":"10.0.3.0/24",
        "Tags" :[ {"Key" : "Name", "Value" : "PrivateSubnet"} ]
        
      }
    }
    
def InternetGateway():
    return {
      "DependsOn": "VPC",
      "Type": "AWS::EC2::InternetGateway",
      "Properties" : {
      "Tags" : [ {"Key" : "Name", "Value" : "InternetGateway"} ]
     }
    }
    
def VpcGatewayAttachment():
    return  {
      "Type": "AWS::EC2::VPCGatewayAttachment",
      "Properties": {
        "InternetGatewayId": {
          "Ref": "InternetGateway"
        },
        "VpcId": {
          "Ref": "VPC"
        }
      }
    }
    
def  PublicSubnet1RouteTable ():
    return {
      "DependsOn": [
        "VPC",
        "InternetGateway"
      ],
      "Type": "AWS::EC2::RouteTable",
      "Properties": {
        "VpcId": {
          "Ref": "VPC"
        },
        "Tags" : [ {"Key" : "Name", "Value" : "PublicSubnet1RouteTable"} ]
        
      }
    }

def  PublicSubnet1RouteTableSubnetAssociation():
    return {
      "DependsOn": [
        "VPC",
        "PublicSubnet1",
        "PublicSubnet1RouteTable"
      ],
      "Type": "AWS::EC2::SubnetRouteTableAssociation",
      "Properties": {
        "RouteTableId": {
          "Ref": "PublicSubnet1RouteTable"
        },
        "SubnetId": {
          "Ref": "PublicSubnet1"
        }
      }
    }

def  PublicSubnet1RouteTableRouteAssociation():
    return {
      "DependsOn": "VpcGatewayAttachment",
      "Type": "AWS::EC2::Route",
      "Properties": {
        "RouteTableId": {
          "Ref": "PublicSubnet1RouteTable"
        },
        "DestinationCidrBlock": "0.0.0.0/0",
        "GatewayId": {
          "Ref": "InternetGateway"
        }
      }
    }
    
def PublicSubnet2RouteTable():
    return  {
      "DependsOn": [
        "VPC",
        "InternetGateway"
      ],
      "Type": "AWS::EC2::RouteTable",
      "Properties": {
        "VpcId": {
          "Ref": "VPC"
        },
      "Tags" : [ {"Key" : "Name", "Value" : "PublicSubnet2RouteTable"} ]
      }
    }

def   PublicSubnet2RouteTableSubnetAssociation():
    return  {
      "DependsOn": [
        "VPC",
        "PublicSubnet2",
        "PublicSubnet2RouteTable"
      ],
      "Type": "AWS::EC2::SubnetRouteTableAssociation",
      "Properties": {
        "RouteTableId": {
          "Ref": "PublicSubnet2RouteTable"
        },
        "SubnetId": {
          "Ref": "PublicSubnet2"
        }
      }
    }

def PublicSubnet2RouteTableRouteAssociation():
    return  {
      "DependsOn": "VpcGatewayAttachment",
      "Type": "AWS::EC2::Route",
      "Properties": {
        "RouteTableId": {
          "Ref": "PublicSubnet2RouteTable"
        },
        "DestinationCidrBlock": "0.0.0.0/0",
        "GatewayId": {
          "Ref": "InternetGateway"
        }
      }
    }

def  ElasticIP():
    return {
      "DependsOn": "InternetGateway",
      "Type": "AWS::EC2::EIP",
      "Properties" : {
      "Tags" : [ {"Key" : "Name", "Value" : "ElasticIP"} ]
        
        }
    }

def NATGateway():
    return  {
      "DependsOn": [
        "ElasticIP",
        "PublicSubnet1"
      ],
      "Type": "AWS::EC2::NatGateway",
      "Properties": {
        "AllocationId": {
          "Fn::GetAtt": [
            "ElasticIP",
            "AllocationId"
          ]
        },
        "SubnetId": {
          "Ref": "PublicSubnet1"
        },
        "Tags" : [ {"Key" : "Name", "Value" : "NatGateway"} ]
      }
    }

def PrivateSubnetRouteTable():
  return {
    "DependsOn": [
        "VPC",
        "NATGateway"
      ],
      "Type": "AWS::EC2::RouteTable",
      "Properties": {
        "VpcId": {
          "Ref": "VPC"
        },
      "Tags" : [ {"Key" : "Name", "Value" : "PrivateSubnetRouteTable"} ]
      }
}

def PrivateSubnetRouteTableSubnetAssociation():
    return {
      "DependsOn": [
        "PrivateSubnetRouteTable",
        "PrivateSubnet"
      ],
      "Type": "AWS::EC2::SubnetRouteTableAssociation",
      "Properties": {
        "RouteTableId": {
          "Ref": "PrivateSubnetRouteTable"
        },
        "SubnetId": {
          "Ref": "PrivateSubnet"
        }
      }
    }

def PrivateSubnetRouteTableRouteAssociation():
    return {
      "DependsOn": [
        "PrivateSubnetRouteTable",
        "NATGateway"
      ],
      "Type": "AWS::EC2::Route",
      "Properties": {
        "RouteTableId": {
          "Ref": "PrivateSubnetRouteTable"
        },
        "DestinationCidrBlock": "0.0.0.0/0",
        "NatGatewayId": {
          "Ref": "NATGateway"
        }
      }
    }
    
def LoadBalancerSecurityGroup():
    return {
      "DependsOn": [
        "VPC",
        "PublicSubnet1",
        "PublicSubnet2"
      ],
      "Type": "AWS::EC2::SecurityGroup",
      "Properties": {
        "GroupDescription": "LoadBalancersecurity group",
        "GroupName": "LoadBalancerSecurityGroup",
        "VpcId": {
          "Ref": "VPC"
        },
        "Tags" : [ {"Key" : "Name", "Value" : "LoadBalancerSecurityGroup"} ],
        "SecurityGroupIngress": [
          {
            "IpProtocol": "tcp",
            "FromPort": "22",
            "ToPort": "22",
            "CidrIp": "0.0.0.0/0"
          },
          {
            "IpProtocol": "tcp",
            "FromPort": "443",
            "ToPort": "443",
            "CidrIp": "0.0.0.0/0"
          },
          {
            "IpProtocol": "tcp",
            "FromPort": "80",
            "ToPort": "80",
            "CidrIp": "0.0.0.0/0"
          }
        ]
      }
    }
    
def WordpressSecurityGroup():
    return  {
      "DependsOn": [
        "VPC",
        "LoadBalancerSecurityGroup"
      ],
      "Type": "AWS::EC2::SecurityGroup",
      "Properties": {
        "GroupDescription": "my security group",
        "GroupName": "WordpressSecurityGroup",
        "VpcId": {
          "Ref": "VPC"
        },
        "Tags" : [ {"Key" : "Name", "Value" : "WordpressSecurityGroup"} ],
        "SecurityGroupIngress": [
          {
            "IpProtocol": "tcp",
            "FromPort": "22",
            "ToPort": "22",
            "CidrIp": "0.0.0.0/0"
          },
          {
            "IpProtocol": "tcp",
            "FromPort": "443",
            "ToPort": "443",
            "SourceSecurityGroupId": {
              "Ref": "LoadBalancerSecurityGroup"
            }
          },
          {
            "IpProtocol": "tcp",
            "FromPort": "80",
            "ToPort": "80",
            "SourceSecurityGroupId": {
              "Ref": "LoadBalancerSecurityGroup"
            }
          }
        ]
      }
    }
    
def MySqlDbSecurityGroup():
    return {
      "DependsOn": [
        "VPC",
        "WordpressSecurityGroup"
      ],
      "Type": "AWS::EC2::SecurityGroup",
      "Properties": {
        "GroupDescription": "Mysql Db security group",
        "GroupName": "DatabaseSecurityGroup",
        "VpcId": {
          "Ref": "VPC"
        },
        "Tags" : [ {"Key" : "Name", "Value" : "MySqlDbSecurityGroup"} ],
        "SecurityGroupIngress": [
          {
            "IpProtocol": "tcp",
            "FromPort": "22",
            "ToPort": "22",
            "SourceSecurityGroupId": {
              "Ref": "WordpressSecurityGroup"
            }
          },
          {
            "IpProtocol": "tcp",
            "FromPort": "3306",
            "ToPort": "3306",
            "SourceSecurityGroupId": {
              "Ref": "WordpressSecurityGroup"
            }
          }
        ]
      }
    }
    
def  WordpressInstance():
    return  {
      "DependsOn": [
        "VPC",
        "PublicSubnet1",
        "PublicSubnet2",
        "InternetGateway",
        "LoadBalancerSecurityGroup",
        "WordpressSecurityGroup"
      ],
      "Type": "AWS::EC2::Instance",
      "Properties": {
        "ImageId": "ami-0885b1f6bd170450c",
        "InstanceType": "t2.micro",
        "KeyName": "PemFile",
        "BlockDeviceMappings": [
          {
            "DeviceName": "/dev/sda1",
            "Ebs": {
              "VolumeSize":"8",
              "VolumeType": "gp2"
            }
          }
        ],
        "NetworkInterfaces": [
          {
            "AssociatePublicIpAddress": "true",
            "DeleteOnTermination":"true",
            "DeviceIndex": "0",
            "GroupSet": [
              {
                "Ref": "WordpressSecurityGroup"
              }
            ],
            "SubnetId": {
              "Ref": "PublicSubnet1"
            }
          }
        ],
        "Tags" : [ {"Key" : "Name", "Value" : "ApacheServer"} ],
        "UserData": {
          "Fn::Base64": {
            "Fn::Join": [
              "\n",
              [
                "#!/bin/bash",
                "sudo apt-get update -y",
                "sudo apt-get upgrade -y",
                "sudo apt-get install apache2 -y",
                "sudo apt-get install mariadb-client -y",
                "sudo apt-get install php libapache2-mod-php php-mysql php-curl php-gd php-json php-zip php-mbstring -y",
                "sudo wget https://wordpress.org/latest.tar.gz",
                "sudo tar -xvzf latest.tar.gz",
                "sudo mv -f wordpress/* /var/www/html",
                "sudo chown -R www-data:www-data /var/www/html",
                "cd /var/www/html",
                "sudo rm index.html",
                "sudo systemctl restart apache2"
              ]
            ]
          }
        }
      }
    }
    
def  WordpressLoadBalancer():
    return {
      "DependsOn": [
        "LoadBalancerSecurityGroup",
        "PublicSubnet1",
        "PublicSubnet2"
      ],
      "Type": "AWS::ElasticLoadBalancingV2::LoadBalancer",
      "Properties": {
        "Name": "WordpressLoadBalancer",
        "SecurityGroups": [
          {
            "Ref": "LoadBalancerSecurityGroup"
          }
        ],
        "Subnets": [
          {
            "Ref": "PublicSubnet1"
          },
          {
            "Ref": "PublicSubnet2"
          }
        ],
        "Type": "application",
        "Tags" : [ {"Key" : "Name", "Value" : "ApacheServerLoadBalancer"} ]
      }
    }
    
def   WordpressTargetGroup():
    return  {
      "DependsOn": [
        "WordpressLoadBalancer",
        "WordpressInstance"
      ],
      "Type": "AWS::ElasticLoadBalancingV2::TargetGroup",
      "Properties": {
        "Name": "WordpressTargetGroup",
        "Port": "80",
        "Protocol": "HTTP",
        "Targets": [
          {
            "Id": {
              "Ref": "WordpressInstance"
            }
          }
        ],
        "TargetType": "instance",
        "VpcId": {
          "Ref": "VPC"
        },
        "Tags" : [ {"Key" : "Name", "Value" : "ApacheServerTargetGroup"} ]
      }
    }

def WordpressLoadBalancerListener():
    return {
      "DependsOn": [
        "WordpressLoadBalancer",
        "WordpressTargetGroup"
      ],
      "Type": "AWS::ElasticLoadBalancingV2::Listener",
      "Properties": {
        "LoadBalancerArn": {
          "Ref": "WordpressLoadBalancer"
        },
        "Port": 80,
        "Protocol": "HTTP",
        "DefaultActions": [
          {
            "Type": "forward",
            "TargetGroupArn": {
              "Ref": "WordpressTargetGroup"
            }
          }
        ]
      }
    }

def  WordpressLaunchConfiguration ():
    return {
      "DependsOn": [
        "WordpressInstance"
      ],
      "Type": "AWS::AutoScaling::LaunchConfiguration",
      "Properties": {
        "LaunchConfigurationName": "WordpressLaunchConfiguration",
        "ImageId": "ami-0885b1f6bd170450c",
        "InstanceId": {
          "Ref": "WordpressInstance"
        },
        "InstanceType": "t2.micro",
        "SecurityGroups": [
          {
            "Ref": "WordpressSecurityGroup"
          }
        ],
        "KeyName": "PemFile",
        "UserData": {
          "Fn::Base64": {
            "Fn::Join": [
              "\n",
              [
                "#!/bin/bash",
                "sudo apt-get update -y",
                "sudo apt-get upgrade -y",
                "sudo apt-get install apache2 -y",
                "sudo apt-get install mariadb-client -y",
                "sudo apt-get install php libapache2-mod-php php-mysql php-curl php-gd php-json php-zip php-mbstring -y",
                "sudo wget https://wordpress.org/latest.tar.gz",
                "sudo tar -xvzf latest.tar.gz",
                "sudo mv -f wordpress/* /var/www/html",
                "sudo chown -R www-data:www-data /var/www/html",
                "cd /var/www/html",
                "sudo rm index.html",
                "sudo systemctl restart apache2"
              ]
            ]
          }
        }
      }
    }
    
def WordpressAutoScalingGroup():
    return {
      "DependsOn": [
        "WordpressLaunchConfiguration"
      ],
      "Type": "AWS::AutoScaling::AutoScalingGroup",
      "Properties": {
        "AutoScalingGroupName": "WordpressAutoScallingGroup",
        "LaunchConfigurationName": {
          "Ref": "WordpressLaunchConfiguration"
        },
        "MinSize": "1",
        "MaxSize": "3",
        "VPCZoneIdentifier": [
          {
            "Ref": "PublicSubnet1"
          },
          {
            "Ref": "PublicSubnet2"
          }
        ],
      }
    }
    
def ScalingPolicy():
    return {
      "Type": "AWS::AutoScaling::ScalingPolicy",
      "Properties": {
        "AutoScalingGroupName": {
          "Ref": "WordpressAutoScalingGroup"
        },
        "PolicyType": "TargetTrackingScaling",
        "TargetTrackingConfiguration": {
          "PredefinedMetricSpecification": {
            "PredefinedMetricType": "ASGAverageCPUUtilization"
          },
          "TargetValue":"70"
        }
      }
    }

def MySqlDbInstance():
    return  {
      "DependsOn": [
        "WordpressInstance",
        "PrivateSubnet",
        "NATGateway",
        "MySqlDbSecurityGroup"
      ],
      "Type": "AWS::EC2::Instance",
      "Properties": {
        "ImageId": "ami-0885b1f6bd170450c",
        "InstanceType":"t2.micro",
        "KeyName": "PemFile",
        "BlockDeviceMappings": [
          {
            "DeviceName": "/dev/sda1",
            "Ebs": {
              "VolumeSize":"8",
              "VolumeType": "gp2"
            }
          }
        ],
        "NetworkInterfaces": [
          {
            "AssociatePublicIpAddress": "false",
            "DeleteOnTermination":"true",
            "DeviceIndex": "0",
            "GroupSet": [
              {
                "Ref": "MySqlDbSecurityGroup"
              }
            ],
            "SubnetId": {
              "Ref": "PrivateSubnet"
            }
          }
        ],
        
        "Tags" : [ {"Key" : "Name", "Value" : "MySqlDatabaseServer"} ],
        "UserData": {
          "Fn::Base64": {
            "Fn::Join": [
              "\n",
              [
                "#!/bin/bash",
                "sudo apt-get update -y",
                "sudo apt-get upgrade -y",
                "sudo apt install mariadb-server -y",
                "sudo systemctl start mariadb",
                "sudo mysql -u root -pjono -e \"create database wordpress;\"",
                "sudo mysql -u root -pjono -e \"create user 'user'@'%' identified by 'password';\"",
                "sudo mysql -u root -pjono -e \"grant all privileges on wordpress.* to 'user'@'%';\"",
                "sudo mysql -u root -pjono -e \"flush privileges;\"",
                "sudo sed -i 's/.*bind-address.*/bind-address = 0.0.0.0/' /etc/mysql/mariadb.conf.d/50-server.cnf",
                "sudo systemctl restart mariadb"
              ]
            ]
          }
        }
      }
    }
    

    
    
    