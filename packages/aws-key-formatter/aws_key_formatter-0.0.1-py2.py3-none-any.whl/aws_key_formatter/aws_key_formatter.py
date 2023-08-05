# -*- coding: utf-8 -*-

"""Main module."""

import argparse
import textwrap

import boto3


def _format_credentials(creds, include_token: bool):
    formatted_str = textwrap.dedent(
        f"""\
        ACCESS_KEY_ID '{creds.access_key}'
        SECRET_ACCESS_KEY '{creds.secret_key}'
        {f"SESSION_TOKEN '{creds.token}'" if include_token else ""}
        """
    ).strip()

    return formatted_str


def _get_creds_from_session(session):
    return session.get_credentials().get_frozen_credentials()


def main(aws_profile: str, include_token: bool):
    session = boto3.Session(profile_name=aws_profile)
    creds = _get_creds_from_session(session)

    formatted_str = _format_credentials(creds, include_token)

    print(formatted_str)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--profile', '-p', default='default', help='AWS CLI Profile name'
    )
    parser.add_argument(
        '--include_token', '-t', action='store_true', help='Include AWS Session Token?'
    )

    args = parser.parse_args()

    main(args.profile, args.include_token)
