# AWSIE

 [![Build Status](https://travis-ci.org/theserverlessway/awsie.svg?branch=master)](https://travis-ci.org/theserverlessway/awsie)
[![PyPI version](https://badge.fury.io/py/awsie.svg)](https://pypi.python.org/pypi/awsie)
[![license](https://img.shields.io/github/license/theserverlessway/awsie.svg)](LICENSE)
[![Coverage Status](https://coveralls.io/repos/github/theserverlessway/awsie/badge.svg?branch=master)](https://coveralls.io/github/theserverlessway/awsie?branch=master)

pronounced /ˈɒzi/ oz-ee like our great friends from down under.

AWSIE is a CloudFormation aware wrapper on top of the AWS CLI. It help you to call an awscli command, but instead of the actual physical ID of the resource you set the logical CloudFormation template id or a CloudFormation Output which will be replaced when executing the actual command.

For many different resources AWS can automatically set a random name when creating the resource through Cloudformation. While this has a big upside with resources not clashing when the same stack gets deployed multipe times, a downside is that running a command against a specific resource means you have to write lookup code or use the resource name by hand.

Awsie helps you to do that lookup and call the awscli without any potential for clashes. By supporting both LogicalIds and Output variables you have a lot of flexibility for your deployment scripts.

## Installation

Before installing make sure you have the awscli installed as awsie depends on it. We don't install it ourselves so you're able to install the exact version you want to use.

```shell
pip3 install awscli
```

awsie can be installed through pip:

```shell
pip3 install awsie
```

Alternatively you can clone this repository and run

```shell
python setup.py install
```

## Quick example

For example when you deploy a CloudFormation stack:

```json
{
    "Resources": {
        "DeploymentBucket": {
            "Type": "AWS::S3::Bucket"
        }
    }
}
```

and then want to list the content of the bucket you can use `awsie`:

```shell
awsie example-stack s3 ls s3://cf:DeploymentBucket: --region us-west-1
```

The first argument needs to be either the Stack Name or a yaml config file with a `stack` parameter that sets the name. This make it compatible to `formica` config files.

```yaml
stack: example-stack
```

```shell
awsie stack.config.yaml s3 ls s3://cf:DeploymentBucket: --region us-west-1
```

or if you want to remove `somefile` from the `DeploymentBucket`:

```shell
awsie example-stack s3 rm s3://cf:DeploymentBucket:/somefile --region us-west-1
```

which will replace `cf:DeploymentBucket:` with the actual name of the resource and run the awscli with all arguments you passed to awsie, except for the stack-name (which has to be the first argument):

```shell
aws s3 ls s3://formica-example-stack-deploymentbucket-1jjzisylxreh9 --region us-west-1
aws s3 rm s3://formica-example-stack-deploymentbucket-1jjzisylxreh9/somefile --region us-west-1
```

## Config File for Stack Name

The first 

## Replacement syntax

The replacement syntax is `cf:LOGICAL_ID:` and will replace LOGICAL_ID with the PhysicalId of the resource through the data returned from list-stack-resources. Make sure you don't forget the second colon at the end, its important to be able to separate the syntax when its embedded in another string.

## Arbitrary commands

You can also use `awsie` to run arbitrary commands with replaced values. Simply use the `--command` to tell awsie not to prepend your commands with `aws`.

```shell
awsie somestack --command awslogs get cf:LogGroup: ALL
```

Sometimes you might want to add environment variables before the command or any other syntax that requires bash, in that case use `bash -c` as a command

```shell
awsie somestack --command bash -c "SOME_ENV=cf:LogGroup: somecommand"
```

## Options

`awsie STACK_NAME`


* `stack`              Has to be the first positional argument and will be removed from call to the AWS cli. Can be either the stack name or a yaml file with a `stack` parameter.
* `--profile PROFILE`  The AWS profile to use for the CloudFormation lookup, will be passed to the aws cli.
* `--region REGION`    The AWS region to use for the CloudFormation lookup, will be passed to the aws cli.
* `--command`          Run your own command instead of an aws cli command.
* `--version`          Print the awsie version.
