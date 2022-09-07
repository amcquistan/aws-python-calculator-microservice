import os

from pydantic import BaseSettings
import boto3
import requests


class Settings(BaseSettings):
  env: str = "local"
  port: int = 8004
  add_endpoint = 'http://localhost:8000/add'
  divide_endpoint = 'http://localhost:8003/divide'

  def http_client(self):
    return requests


def configure() -> Settings:
  normalized_fields = { k.lower(): k for k in Settings.__fields__.keys() }
  
  awsenv = { k.lower()[8:]: v for k, v in os.environ.items() if k.lower().startswith('aws_ssm_') }
  aws_ssm_fields = normalized_fields.keys() & awsenv.keys()

  if not aws_ssm_fields:
      return Settings()

  ssm = boto3.client('ssm')
  fields = {}
  for field in aws_ssm_fields:
      response = ssm.get_parameter(Name=awsenv[field])
      fields[normalized_fields[field]] = response['Parameter']['Value']

  return Settings(**fields)

