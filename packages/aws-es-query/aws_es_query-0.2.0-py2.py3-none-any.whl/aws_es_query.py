import json

import click

import boto3
import requests
from requests_aws4auth import AWS4Auth


@click.command()
@click.option("--role-arn", required=True, type=str)
@click.option("-X", required=False, type=str, default="GET")
@click.argument("url")
def main(role_arn, x, url):
    sts = boto3.client("sts")
    resp = sts.assume_role(RoleArn=role_arn, RoleSessionName="es-curl")
    awsauth = AWS4Auth(
        resp["Credentials"]["AccessKeyId"],
        resp["Credentials"]["SecretAccessKey"],
        "eu-west-1",
        "es",
        session_token=resp["Credentials"]["SessionToken"],
    )

    response = requests.request(x, url, auth=awsauth)

    try:
        print(json.dumps(response.json(), indent=4, sort_keys=True))
    except json.JSONDecodeError:
        print(response.content.decode("utf-8"))


if __name__ == "__main__":
    main()
