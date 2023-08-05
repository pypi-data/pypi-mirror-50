# aws-manifest

A python package for retrieving information about aws's api manifest consisting
of resources and their actions.

## Getting Started

`pip3 install aws-manifest`

## Usage

```
from awsmanifest import manifest, AwsManifest

# Retrieve the latest set of aws resources
m = manifest()
print(m["serviceMap"]["Amazon Ec2]["Actions])

# Retrieve the bundled local copy of aws resources
m = manifest(local=True)
...

# For helper functions, use the `AwsManifest` class
a = AwsManifest()
print(a.service_prefixes())
print(a.actions("Amazon Ec2))
print(a.actions("s3))
...
```

# Licensing

MIT